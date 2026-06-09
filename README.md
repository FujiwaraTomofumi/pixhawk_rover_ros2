# pixhawk_rover_ros2
Pixhawkを載せたローバーをROS2化する

## ローバー
- CuboRex CuGo V3
- Pixhawk 2.4.8: 

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

