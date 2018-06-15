import os

from aiohttp import web
import aiohttp

from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp

from . import pull_request
from . import comments

router = routing.Router(pull_request.router, comments.router)


async def test(request):
    return web.Response(status=200, text="Hello world!")


async def main(request):
    # read the GitHub webhook payload
    body = await request.read()

    # our authentication token and secret
    oauth_token = os.environ.get("GH_TOKEN")

    # a representation of GitHub webhook event
    event = sansio.Event.from_http(request.headers, body)

    # instead of mariatta, use your own username
    async with aiohttp.ClientSession() as session:
        gh = gh_aiohttp.GitHubAPI(session, "barrachri",
                                  oauth_token=oauth_token)

        # call the appropriate callback for the event
        await router.dispatch(event, gh)

    # return a "Success"
    return web.Response(status=200)

if __name__ == "__main__":
    app = web.Application()
    app.router.add_get("/test", test)
    app.router.add_post("/", main)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)

    web.run_app(app, port=port)
