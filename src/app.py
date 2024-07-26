from fastapi import FastAPI
from pydantic import BaseModel
from ray.serve.handle import DeploymentHandle


class TextRequest(BaseModel):
    text: str


class PairRequest(BaseModel):
    pair: list[str]


def create_app(
    vectoriser_handle: DeploymentHandle,
    reranker_handle: DeploymentHandle,
    composite_handle: DeploymentHandle,
) -> FastAPI:
    app = FastAPI()

    @app.post("/vectorise")
    async def vectorise(request: TextRequest):
        result = await vectoriser_handle.remote(request.text)
        return {"vector": result}

    @app.post("/rerank")
    async def rerank(request: PairRequest):
        result = await reranker_handle.remote(request.pair)
        return {"ranking_score": result}

    @app.post("/composite")
    async def composite(request: TextRequest):
        result = await composite_handle.remote(request.text)
        return {"composite": result}

    return app
