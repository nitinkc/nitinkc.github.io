---
categories:
- Developer Tools
date: 2024-09-23 21:14:00
tags:
- Compiler
- MacOS
- Installation
title: GCC Cross Compiler - Mac installation
---

# Creating a Cross compiler on Mac

### Download
- binutils-2.43.tar.xz 2024-08-04 11:05
    - [https://ftp.gnu.org/gnu/binutils/](https://ftp.gnu.org/gnu/binutils/)
- GCC gcc-14.2.0 - 2024-08-01
    - https://ftp.gnu.org/gnu/gcc/

```shell
mkdir -p $HOME/opt/cross

export PREFIX="$HOME/opt/cross"
export TARGET=i686-elf
export PATH="$PREFIX/bin:$PATH"

mkdir src && cd src

# Keep the build files of binutils

mkdir build-binutils && cd build-binutils
../binutils-2.43/configure --target==$TARGET --prefix=="$PREFIX" --with-sysroot
--disable-nls --disable-werror
make
make install
```

### Build GCC

```shell
mkdir build-gcc   
cd build-gcc  
../gcc-14.2.0/configure --target=$TARGET --prefix=$PREFIX --disable-nls --enable-languages=c,c++ --without-headers

make clean
make all-gcc
make all-target-libgcc
```

The required libraries for MacBook. It is better to use Ubuntu to be able to develop seemlessly
```shell
brew install build-essesntial
brew install bison
brew install flex
brew install libgmp3-dev
brew install libmpc
brew install texinfo
brew install libidl 
```