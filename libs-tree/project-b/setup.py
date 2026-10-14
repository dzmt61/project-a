from setuptools import setup, find_packages


setup(
  name="project-b",
  version="1.0.0",
  packages=find_packages(where="src"),
  package_dir={"": "src"},
  author="Not Important",
  description="date & str utils",
  python_requires=">=3.11",
)