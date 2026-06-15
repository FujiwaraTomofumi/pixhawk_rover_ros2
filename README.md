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


