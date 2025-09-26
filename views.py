from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Repository
from .serializers import RepoSerializer
from .git_utils import init_bare_repo, commit_file
class RepoViewSet(viewsets.ModelViewSet):
    queryset=Repository.objects.all()
    serializer_class=RepoSerializer
    def perform_create(self, serializer):
        repo=serializer.save(owner=self.request.user)
        init_bare_repo(self.request.user.username, repo.name)
    @action(detail=True, methods=['post'])
    def commit(self, request, pk=None):
        repo=self.get_object()
        branch=request.data.get('branch','main')
        path=request.data.get('path')
        content=request.data.get('content','')
        message=request.data.get('message','Update via web')
        try:
            oid=commit_file(repo.owner.username, repo.name, branch,
                            request.user.get_full_name() or request.user.username,
                            request.user.email or 'no-reply@example.com',
                            path, content, message)
            return Response({'oid':oid})
        except Exception as e:
            return Response({'error':str(e)}, status=status.HTTP_400_BAD_REQUEST)
