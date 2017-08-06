
```
$ sudo mount -o loop kimberly.img ./mounted
```



```
tbkim@ubuntu:~/ctfing/2017_sha/forensic$ ls -al --time-style=full-iso ./mounted/Pictures/
total 29123
drwxrwxr-x  2 1001 1001    1024 2017-06-20 08:04:04.000000000 -0700 .
drwxr-xr-x 12 1001 1001    1024 2017-06-20 09:55:16.000000000 -0700 ..
-rw-r--r--  1 1001 1001 1040070 2017-06-20 09:14:40.000000000 -0700 78d14f37ae413511b119776c2294c414.png
-rw-r--r--  1 1001 1001 1747640 2017-06-20 09:14:42.000000000 -0700 8210680-Palomino-Shetland-pony-Equus-caballus-3-years-old-standing-in-front-of-white-background-Stock-Photo.png
-rw-r--r--  1 1001 1001 1262073 2017-06-20 09:14:42.000000000 -0700 8210722-Palomino-Shetland-pony-Equus-caballus-3-years-old-standing-in-front-of-white-background-Stock-Photo.png
-rw-r--r--  1 1001 1001 2194500 2017-06-20 09:14:38.000000000 -0700 bay_pony_cantering_2_by_tamacilo.png
-rw-r--r--  1 1001 1001 2144707 2017-06-20 09:14:41.000000000 -0700 bay_pony_rolling2_by_tamacilo.png
-rw-r--r--  1 1001 1001 1316679 2017-06-20 09:14:40.000000000 -0700 connemara_pony2_750.png
-rw-r--r--  1 1001 1001  645968 2017-06-20 09:14:41.000000000 -0700 dappled-pony.png
-rw-r--r--  1 1001 1001  947739 2017-06-20 09:14:41.000000000 -0700 f09086061f03f080d0851d9154e11653.png
-rw-r--r--  1 1001 1001 1564211 2017-06-20 09:14:41.000000000 -0700 Het-verschil-tussen-een-pony-en-een-shetland-pony.png
-rw-r--r--  1 1001 1001 1442577 2017-06-20 09:14:40.000000000 -0700 oli.png
-rw-r--r--  1 1001 1001  947331 2017-06-20 09:14:40.000000000 -0700 Peppermint-Pony.png
-rw-r--r--  1 1001 1001 3478821 2017-06-20 09:14:39.000000000 -0700 pony.png
-rw-r--r--  1 1001 1001 1916939 2017-06-20 09:14:38.000000000 -0700 pony_shutterstock_50279794.png
-rw-r--r--  1 1001 1001 1910486 2017-06-20 09:14:42.000000000 -0700 shetlander-pony.png
-rw-r--r--  1 1001 1001  832413 2017-06-20 09:14:39.000000000 -0700 shutterstock_146544482-680x400.png
-rw-r--r--  1 1001 1001 2111020 2017-06-20 09:14:40.000000000 -0700 white-pony-951772_960_720.png
-rw-r--r--  1 1001 1001 4308839 2017-06-20 09:14:39.000000000 -0700 Wild_Pony_Assateague.png

```