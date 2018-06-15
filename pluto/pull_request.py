import gidgethub.routing

router = gidgethub.routing.Router()

@router.register("pull_request", action="opened")
async def pull_request_opened_event(event, gh, *args, **kwargs):
    """ Whenever an issue is opened, greet the author and say thanks."""

    url = event.data["pull_request"]["comments_url"]
    author = event.data["pull_request"]["user"]["login"]

    title = event.data["pull_request"]["title"]
    body = event.data["pull_request"]["body"]

    message = f"Thanks for the report @{author}! I will look into it ASAP! (I'm a bot)."
    await gh.post(url, data={"body": message})


@router.register("pull_request", action="closed")
async def delete_branch(event, gh, *args, **kwargs):
    """
    Delete the branch once miss-islington's PR is closed.
    Say thanks if it's merged.
    """
    if event.data["pull_request"]["merged"]:
        issue_number = event.data['pull_request']['number']
        merged_by = event.data['pull_request']['merged_by']['login']

        url = event.data["pull_request"]["comments_url"]

        await gh.post(url, data={"body": f"Thanks, @{merged_by}!")

        branch_name = event.data['pull_request']['head']['ref']
        repository = event.data['repository']['"full_name"']

        url = f"/repos/{repository}/git/refs/heads/{branch_name}"

        await gh.delete(url)
