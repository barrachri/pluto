import gidgethub.routing

router = gidgethub.routing.Router()

@router.register("issue_comment", action="created")
async def pull_request_opened_event(event, gh, *args, **kwargs):
    """ Whenever an issue is opened, greet the author and say thanks."""

    url = event.data["issue"]["comments_url"]

    author = event.data["comment"]["user"]["login"]
    body = event.data["comment"]["body"]

    message = f"That not clear @{author}! \n > {body}"
    await gh.post(url, data={"body": message})

