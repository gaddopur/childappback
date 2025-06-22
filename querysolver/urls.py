from django.urls import path
from django.conf.urls.static import static
from childappback import settings
from .views import QuerySolver, SummarizePdfView, MathSolver, SchoolBookSummaryView, AvailableSummaryOptionsView, FileExplorerView, NestedOptionsView

urlpatterns = [
    path('solvequery/', QuerySolver.as_view({'post': 'solveQuery'}), name='solve_query'),
    path('pdf_summerizer/', SummarizePdfView.as_view(), name='summarize_pdf'),
    path('math_solver/', MathSolver.as_view(), name='math_solver'),
    path('school-book-summary/', SchoolBookSummaryView.as_view(), name='school-book-summary'),
    path('available-summary-options/', AvailableSummaryOptionsView.as_view(), name='available_summary_options'),
    path('file-explorer/', FileExplorerView.as_view(), name='file_explorer'),
    path('nested-options/', NestedOptionsView.as_view(), name='nested_options'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)