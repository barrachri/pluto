import gidgethub.routing

router = gidgethub.routing.Router()

@router.register("pull_request", action="opened")
async def pull_request_opened_event(event, gh, *args, **kwargs):
    """ Whenever an issue is opened, greet the author and say thanks."""

    url = event.data["pull_request"]["comments_url"]
    author = event.data["pull_request"]["user"]["login"]

    message = f"Thanks for the report @{author}! I will look into it ASAP! (I'm a bot)."
    await gh.post(url, data={"body": message})
