import setuptools

setuptools.setup(
    name="TKUCourseSelectionSDK",
    version="0.0.3",
    author="isekai",
    description="Tools for auto selecting course of TKU",
    url="https://github.com/Isekai-Seikatsu/TKUCourseSelectionSDK",
    install_requires=["requests", "parsel", "click"],
    py_modules=["course_selection", "data_parsing", "adding_script"],
    entry_points='''
        [console_scripts]
        tku_course_select=adding_script:cli
    ''',
    python_requires='>=3.6',
)
