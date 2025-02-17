from dishka import Provider, Scope, provide

from user.dal import UserCrud, UserRepo


class UserProvider(Provider):
    crud = provide(UserCrud, scope=Scope.REQUEST)
    repo = provide(UserRepo, scope=Scope.REQUEST)
