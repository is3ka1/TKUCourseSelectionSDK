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
### Loop adding
```
cat > course_list.txt <<EOF
+ xxxx
+ xxxx
+ xxxx
EOF

docker run --rm -it --env-file .env -v `pwd`/course_list.txt:/course_list.txt isekai/tku_course_select --loop
```

### Interactive
`docker run --rm -it isekai/tku_course_select -`
```
❯ docker run --rm -it isekai/tku_course_select -
Student ID: 406410380
Password:
+7000
[2021-03-02T14:35:34.190252] [action#0] course_id: 7000
msg: E999 加選失敗???E044 所選的開課序號不存在, 請查核....... 請輸入開課序號後, 再按功能鍵...

?0700
[2021-03-02T14:35:40.532055] [action#1] course_id: 0700
msg: I000 查詢開課序號資料成功!!!.... 請輸入開課序號後, 再按功能鍵...

-0700
[2021-03-02T14:35:49.322929] [action#2] course_id: 0700
msg: E999 退選失敗???E046 退選的開課序號未選或已退選, 請查核....... 請輸入開課序號後, 再按功能鍵...
```

### Demo
[![recording](https://asciinema.org/a/xuhczftfqDfkNwv4jXhnn22OU.svg)](https://asciinema.org/a/xuhczftfqDfkNwv4jXhnn22OU)

### Examples

or try scripts in [examples](https://github.com/Isekai-Seikatsu/TKUCourseSelectionSDK/tree/master/examples):

`python -m examples.simple_interactive_cli`
`python -m examples.loop_add_course`
