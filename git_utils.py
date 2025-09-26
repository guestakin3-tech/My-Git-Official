import os, shutil, tempfile
from django.conf import settings
import pygit2
def repo_fs_path(owner, repo_name):
    root=settings.GIT_REPOS_ROOT
    path=os.path.join(root, owner, f"{repo_name}.git")
    return path
def init_bare_repo(owner, repo_name):
    path=repo_fs_path(owner, repo_name)
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        repo=pygit2.init_repository(path, bare=True)
        return repo
    else:
        return None
def clone_repo_to_workdir(owner, repo_name, workdir):
    bare=repo_fs_path(owner, repo_name)
    return pygit2.clone_repository(f"file://{bare}", workdir)
def commit_file(owner, repo_name, branch, author_name, author_email, file_path_in_repo, content, message):
    tmp=tempfile.mkdtemp()
    try:
        work_repo=clone_repo_to_workdir(owner, repo_name, tmp)
        try:
            ref=work_repo.lookup_reference(f"refs/heads/{branch}")
        except KeyError:
            if work_repo.head_is_unborn:
                builder=work_repo.TreeBuilder()
                tree=builder.write()
                author=pygit2.Signature(author_name, author_email)
                committer=author
                oid=work_repo.create_commit('HEAD', author, committer, message, tree, [])
            else:
                work_repo.create_branch(branch, work_repo.head.peel())
            work_repo.checkout(branch)
        else:
            work_repo.checkout(ref)
        fs_path=os.path.join(tmp, file_path_in_repo)
        os.makedirs(os.path.dirname(fs_path), exist_ok=True)
        with open(fs_path,'w',encoding='utf-8') as f:
            f.write(content)
        work_repo.index.add(file_path_in_repo)
        work_repo.index.write()
        tree=work_repo.index.write_tree()
        author=pygit2.Signature(author_name, author_email)
        committer=author
        parents=[]
        if not work_repo.head_is_unborn:
            parents=[work_repo.revparse_single('HEAD').oid]
        oid=work_repo.create_commit(f"refs/heads/{branch}", author, committer, message, parents)
        remote=work_repo.remotes['origin']
        remote.push([f"refs/heads/{branch}:refs/heads/{branch}"])
        return oid.hex
    finally:
        shutil.rmtree(tmp)
