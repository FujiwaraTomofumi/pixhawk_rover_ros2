# pixhawk_rover_ros2
Pixhawkを載せたローバーをROS2化する

## ローバー
- CuboRex CuGo V3
- Pixhawk 2.4.8 (ファームウェア: ArduRover 4.6.3)

## 環境
- Ubuntu 22.04 LTS
- ROS 2 Humble
- Python関係：pymavlink, pyserial

## 実行方法
1. USBケーブルでPixhawkとPCをつなぐ。
1. PCにジョイスティックをつなぐ。
1. ローバーにバッテリーをつなぐ。
1. Pixhawkのセーフティスイッチを長押しする。
1. ラジコン送信機のスイッチを入れる。
1. ROSノードを起動する。  
    ```bash
    ros2 launch cmd_vel_to_pixhawk joystick.launch.py 
    ```

    - ○: ARM化
    - ×: DISARM化
    - R1: セーフティボタン
    - 左スティック上下：前進後退
    - 右スティック左右：旋回



## Ubuntu
ラズパイ4で動かす。
- Ubuntu 22.04: もっさりしていた。ROS2 Humbleもオーバーヘッドが大きくて遅い感触があった。
- Ubuntu 24.04: Serverを入れてからMATE Desktopを入れるらしい。ROS2 Jazzyは同等か高速らしい。

## ServerからMATEインストール
1. Raspberry Pi ImagerでUbuntu 24.04 Serverをインストールする。 
2. ログイン後
  ```bash
  sudo apt update
  sudo apt upgrade
  sudo apt install ubuntu-mate-desktop
  ```
  としたが、依存関係の問題が出てインストールできない。

Imagerで出てくるUbuntu 24.04 Desktopを入れてみるか…

### 追記
リポジトリにnoble-updates, noble-backportsを追加してやってみる。

```bash
sudo nano /etc/apt/sources.list.d/ubuntu.sources
```
以下の`Suites: `のところに、nobleしか記述がない。ここにnoble-updates noble-backportsを追加して保存する。(Ctrl-S, Ctrl-X)
```bash
Types: deb
URIs: http://ports.ubuntu.com/ubuntu-ports
Suites: noble noble-updates noble-backports
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

Types: deb
URIs: http://ports.ubuntu.com/ubuntu-ports
Suites: noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

この後、
```bash
sudo apt update
sudo apt upgrade
```

として再起動。

```bash
sudo apt install mate-desktop-environment-core
```

としたら成功した。

再起動してもGUIが出ない。

```bash
sudo apt install lightdm
```

として途中でDefault display managerと聞かれたらlightdmを選択。

## 24.04 Desktop版を入れる
動いた。
けど少しカクカクしているような…

22.04を入れてMATEにしてみるか…

## 22.04 Server -> MATE
22.04 Serverを入れた。

アップデート
```bash
sudo apt update
sudo apt upgrade
```


```bash
sudo apt install ubuntu-mate-core
```

とすると、最小構成が入るらしい。

これで端末を起動すると早かった。
が、ROS2 Humbleを入れて、`.bashrc`にROSの`setup.bash`をソースするように記述したら、端末起動に時間がかかるようになった…

起動時に120s待つようになっているので、ネットワークの設定を変える。
```bash
sudo systemctl disable systemd-networkd-wait-online.service
sudo systemctl mask systemd-networkd-wait-online.service
```
これでも30sくらい待っているが…？

## Pixhawk載せたローバー制御方法
ROS2で動かす方法
1. RC入力を上書きする

    `RC_CHANNELS_OVERRIDE`を設定する。



1. MANUAL_CONTROLを使う


1. GUIDEDモードで速度司令

    多分QAVでやっていた方法。


Pixhawkとラズパイつなぎ方
1. USB接続（かんたん）
1. シリアル接続  
    Pixhawk TELEM2 <-> ラズパイUART  
    - TX -- RX (GPIO15)  
    - RX -- TX (GPIO14)  
    - GND -- GND  

USBでつないでテストする。

### RC入力を上書きする

- cmd_vel.linear.x: スロットル
- cmd_vel.angular.z: ステアリング

に変換して、MAVLinkの`RC_CHANNEL_OVERRIDE`に送る。

1. USBでPixhawkとラズパイをつなぐ。  
    `ls /dev/ttyACM0 -la`として確認する。`AMA0`というのもあるが…

    groupsで見ると、すでに`rover`と`dialout`が同じグループになっている？権限の変更は不要？

2. ラズパイで作業  
    ```bash
    sudo apt install python3-pip
    pip3 install pymavlink
    pip3 install pyserial
    ```

    テストスクリプト作成

    接続チェック (connection_check.py)
    ```py
    from pymavlink import mavutil

    master = mavutil.mavlink_connection('/dev/ttyACM0')

    master.wait_heartbeat()

    print("connected")
    print(master.target_system)
    ```
    実行
    ```bash
    python3 connection_check.py
    ```

    - バッテリーつなぐ
    - PixhawkスイッチON
    - 送信機ON  
    にした後、アーム化 (arm.py) 実行
    ```bash
    python3 arm.py
    ```
    ARM成功！

    ディスアーム化 (disarm.py) 実行
    ```bash
    python3 disarm.py
    ```
    DISARM成功。

    前進 (forward.py) テスト
    ```bash
    python3 forward_test.py
    ```
    前進も成功。

    `/cmd_vel`で遠隔操作するノード
    ```bash
    ros2 run cmd_vel_to_pixhawk cmd_vel_to_pixhawk
    ```

    ジョイスティックで遠隔操作
    ```bash
    ros2 launch cmd_vel_to_pixhawk joystick.launch.py
    ```

    - ○: ARM化
    - ×: DISARM化
    - R1: セーフティボタン
    - 左スティック上下：前進後退
    - 右スティック左右：旋回

## ラズパイをバッテリーで駆動して動かす
### リモートデスクトップの設定


操作用ノートPCとラズパイの両方で以下を実行する。

```bash
sudo apt install xserver-xorg-core xorgxrdp xrdp
```

以下はラズパイのみ

`/etc/xrdp/xrdp.ini`を修正する．

```bash
sudo nano /etc/xrdp/xrdp.ini
```
で開いて、
`new_cursors=true` を探して　`new_cursors=false`　に変更。
`Ctrl + S`, `Ctrl + X` で保存して終了。

`/etc/xrdp/startwm.sh`も同様に開いて以下を追記する．
```bash
sudo nano /etc/xrdp/startwm.sh
```
```sh
unset DBUS_SESSION_BUS_ADDRESS
exec mate-session

test -x /etc/X11/Xsession && exec /etc/X11/Xsession (これは元の行)
exec /bin/sh /etc/X11/Xsession (これは元の行)
```

「カラープロファイルを作成するには認証が必要です」と出てくる場合は以下で対処する。

#### 認証を消すには以下を実施
参考）
　https://tarufu.info/ubuntu_xrdp_color_profile/  
　https://tech.nkhn37.net/ubuntu-xrdp-remove-dialog/

`/etc/polkit-1/localauthority.conf.d/02-allow-colord.conf`
が存在していれば削除する。
```bash
sudo rm /etc/polkit-1/localauthority.conf.d/02-allow-colord.conf
```
→なかったので削除不要

新しいファイルを作成  
ルートになって
```bash
sudo -i
nano /etc/polkit-1/localauthority/50-local.d/45-allow-colord.pkla
```

内容は以下
```
[Allow Colord all Users]
Identity=unix-user:*
Action=org.freedesktop.color-manager.create-device;org.freedesktop.color-manager.create-profile;org.freedesktop.color-manager.delete-device;org.freedesktop.color-manager.delete-profile;org.freedesktop.color-manager.modify-device;org.freedesktop.color-manager.modify-profile
ResultAny=no
ResultInactive=no
ResultActive=yes

[Allow Package Management all Users]
Identity=unix-user:*
Action=org.debian.apt.*;io.snapcraft.*;org.freedesktop.packagekit.*;com.ubuntu.update-notifier.*
ResultAny=no
ResultInactive=no
ResultActive=yes
```

保存してサービス再起動
```bash
sudo systemctl restart polkit.service
```

#### ラズパイをホットスポットにする

    ```bash 
    nmcli device wifi hotspot ifname wlan0 ssid RoverPi password 12345678
    ```
これでRoverPiというSSIDのホットスポットができる。パスワードは12345678。

#### IPを割り当てる  
ラズパイ側

```bash
nm-connection-editor
```
としてHotspotを編集。

IP: 10.1.13.50/24  
GW: 10.1.13.1

優先的に自動接続するにチェックを入れて、99に設定。自動で起動するようにしておく。


一度ホットスポットを再起動する。
```bash
nmcli connection down Hotspot 
nmcli connection up Hotspot 
```

#### ノートPCからログインできるようにする

WiFIのSSIDから「RoverPi」を探して接続する。
```bash
nm-connection-editor
```
としてRoverPiを編集。

IP: 10.1.13.100/24  
GW: 10.1.13.1

この状態でRemminaを起動して、RDPで接続を作成。

### SSHの設定
なにかあったらSSHでリモート接続もできるようにしておく。

両方にインストールする
```bash
sudo apt-get install openssh-server
```

ラズパイにsshを入れると、パスワードログインが無効になっていたので以下を実行する。

```bash
sudo nano 
```

RoverPiへの接続（ノートPCから）※ホットスポットに接続して
```bash
ssh -p 22 rover@10.1.13.50
```


