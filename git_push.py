def git_push():
    """
    This function is complete. Stages, commits, and pushes new images to your GitHub repo.
    """
    try:
        repo = Repo(REPO_PATH)
        origin = repo.remote("origin")
        print("added remote")
        origin.pull()
        print("pulled changes")
        repo.git.add(REPO_PATH + FOLDER_PATH)
        repo.index.commit("New Photo")
        print("made the commit")
        origin.push()
        print("pushed changes")
    except:
        print("Couldn't upload to git")