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


