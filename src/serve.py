import ray

from ray import serve
from ray.serve.handle import DeploymentHandle
from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder


CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
VECTORISER_MODEL = "sentence-transformers/all-MiniLM-L12-v2"
NUM_REPLICAS = 1
MAX_ONGOING_REQUESTS = 1


@serve.deployment(num_replicas=NUM_REPLICAS, max_ongoing_requests=MAX_ONGOING_REQUESTS)
class Vectoriser:
    def __init__(self):
        self.vectoriser_model = SentenceTransformer(model_name_or_path=VECTORISER_MODEL, device="cpu")

    @serve.batch(max_batch_size=MAX_ONGOING_REQUESTS)
    async def __call__(self, pairs: list[list]):
        return self.vectoriser_model.encode(pairs).tolist()


@serve.deployment(num_replicas=NUM_REPLICAS, max_ongoing_requests=MAX_ONGOING_REQUESTS)
class Reranker:
    def __init__(self):
        self.reranker_model = CrossEncoder(model_name=CROSS_ENCODER_MODEL, device="cpu")

    @serve.batch(max_batch_size=MAX_ONGOING_REQUESTS)
    async def __call__(self, pairs: list[list]):
        return self.reranker_model.predict(pairs).tolist()


@serve.deployment(num_replicas=NUM_REPLICAS, max_ongoing_requests=MAX_ONGOING_REQUESTS)
class InnerModel1:
    async def __call__(self, text: str):
        return text + " from InnerModel1"


@serve.deployment(num_replicas=NUM_REPLICAS, max_ongoing_requests=MAX_ONGOING_REQUESTS)
class InnerModel2:
    async def __call__(self, text: str):
        return text + " from InnerModel2"


@serve.deployment(num_replicas=NUM_REPLICAS, max_ongoing_requests=MAX_ONGOING_REQUESTS)
class CompositeModel:
    def __init__(self, inner_model1, inner_model2):
        self.inner_model1 = inner_model1
        self.inner_model2 = inner_model2

    async def __call__(self, text: str):
        not_awaited_response1 = self.inner_model1.remote(text)
        response2 = await self.inner_model2.remote(not_awaited_response1)
        # Also possible is to call them in parallel and await both responses
        return response2


def create_handles() -> dict[str, DeploymentHandle]:
    ray.init(dashboard_host="0.0.0.0", dashboard_port=3000)
    vectoriser_handle = serve.run(Vectoriser.bind(), name="vectoriser", route_prefix="/vectorise")
    reranker_handle = serve.run(Reranker.bind(), name="reranker", route_prefix="/rerank")
    composite_handle = serve.run(
        CompositeModel.bind(InnerModel1.bind(), InnerModel2.bind()),
        name="composite",
        route_prefix="/composite",
    )

    return {
        "vectoriser_handle": vectoriser_handle,
        "reranker_handle": reranker_handle,
        "composite_handle": composite_handle,
    }
