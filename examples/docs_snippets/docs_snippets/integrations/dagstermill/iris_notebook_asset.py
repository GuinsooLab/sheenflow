from sheenflowmill import define_dagstermill_asset

from sheenflow import file_relative_path

iris_kmeans_notebook = define_dagstermill_asset(
    name="iris_kmeans",
    notebook_path=file_relative_path(__file__, "../notebooks/iris-kmeans.ipynb"),
)
