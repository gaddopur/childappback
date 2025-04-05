from django.urls import path
from .views import QuerySolver

urlpatterns = [
    path('solvequery/', QuerySolver.as_view({'post': 'solveQuery'}), name='solve_query'),
]