# TKUCourseSelectionSDK
TKU course selecting tools

## Installation
`docker pull isekai/tku_course_select`

## Quickstart
### Help
```
docker run --rm isekai/tku_course_select --help
Usage: tku_course_select [OPTIONS] [SCRIPT]

Options:
  --studid TEXT
  --password TEXT
  -v, --verbose
  --loop / --no-loop
  --help              Show this message and exit.

```
### Credentials
with optional arguments `--stuid` and `--password `, you can also leave them in environment variables `STUID` and `PASSWD`.
If not given, enter in prompt ask.

### Execute script
```
+ : Add course
- : Delete course
? : Get course info
```

```
tku_course_select - <<EOF
+ 0700
- 0700
? 0700
EOF
```
`tku_course_select -v --loop course_list_file.txt`




### Examples

or try scripts in [examples](https://github.com/Isekai-Seikatsu/TKUCourseSelectionSDK/tree/master/examples):

`python -m examples.simple_interactive_cli`
`python -m examples.loop_add_course`
