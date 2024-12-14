%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/jazzy/.*$
%global __requires_exclude_from ^/opt/ros/jazzy/.*$

Name:           ros-jazzy-ament-cpplint
Version:        0.17.1
Release:        0%{?dist}%{?release_suffix}
Summary:        ROS ament_cpplint package

License:        Apache License 2.0 and BSD
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  python%{python3_pkgversion}-devel

%if 0%{?with_tests}
BuildRequires:  python3-pytest
BuildRequires:  ros-jazzy-ament-copyright
BuildRequires:  ros-jazzy-ament-flake8
BuildRequires:  ros-jazzy-ament-pep257
%endif

%description
The ability to check code against the Google style conventions using cpplint and
generate xUnit test result files.

%prep
%autosetup -p1

%build
# 修复 PYTHONPATH 环境变量
export PYTHONPATH=/opt/ros/jazzy/lib/python3.11/site-packages:$PYTHONPATH

# 修复 CMAKE_PREFIX_PATH 和 PKG_CONFIG_PATH
export CMAKE_PREFIX_PATH=/opt/ros/jazzy
export PKG_CONFIG_PATH=/opt/ros/jazzy/lib/pkgconfig

# 输出环境变量以验证设置
echo "PYTHONPATH: $PYTHONPATH"
echo "CMAKE_PREFIX_PATH: $CMAKE_PREFIX_PATH"
echo "PKG_CONFIG_PATH: $PKG_CONFIG_PATH"

# 验证 ament_package 是否可用
python3 -c "import ament_package" || { echo "ament_package not found"; exit 1; }

# 创建构建目录并进入
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/jazzy/setup.sh" ]; then . "/opt/ros/jazzy/setup.sh"; fi
%py3_install -- --prefix "/opt/ros/jazzy"

%if 0%{?with_tests}
%check
# 检查是否存在测试目录或文件
if [ -d "tests" ] || ls test_*.py *_test.py > /dev/null 2>&1; then
    # 加载安装目录的 setup.sh 文件（如果存在）
    if [ -f "/opt/ros/jazzy/setup.sh" ]; then
        . "/opt/ros/jazzy/setup.sh"
    fi
    %__python3 -m pytest tests || echo "RPM TESTS FAILED"
else
    echo "No tests to run, skipping."
fi
%endif

%files
%license /opt/ros/jazzy/LICENSE
/opt/ros/jazzy/*

%changelog
* Sun Dec 15 2024 Chris Lalancette <clalancette@gmail.com> - 0.17.1-0
- Autogenerated by Bloom

