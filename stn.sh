#!/usr/bin/expect
#trap sigwinch spawned
trap {
 set rows [stty rows]
 set cols [stty columns]
 stty rows $rows columns $cols < $spawn_out(slave,name)
} WINCH


set ip [lindex $argv 0]

spawn ssh root@127.0.0.$ip

expect {
"*yes/no" { send "yes\r"; exp_continue}
"*password:" { send "123\r" }
}
interact
