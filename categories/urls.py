from django.urls import path

from .views      import CategoryView, SubCategoryView, TypeView

urlpatterns = {
  path('category', CategoryView.as_view()),
  path('subcategory/<int:category_id>/<int:subcategory_id>', SubCategoryView.as_view()),
  path('type', TypeView.as_view())gr
  # path('csv', CsvView.as_view())
}