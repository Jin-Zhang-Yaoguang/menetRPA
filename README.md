# menetRPA


@startuml

start
partition 初始化 {
    :           账号: 账号、密码           ;
	  : 链接：登录链接、目标页面链接  ;
    :     参数: 开始页面、结束页面     ;
}

partition 登录初始化 {
    :  登录：输入账号密码、点击登录  ;
    :          进入：进入目标页面         ;
}
partition 获取目标范围页面数据 {
    :获取当前页面;
	  if (当前页面=开始页面) then (true)
    else
        :修改html将当前页面改为开始页面数;
				:点击修改后的页面数;
    endif

		while (当前页面 < 结束页面) is (true)
    	  :获取当前页面数;
				:获取page_source并存储;
				:点击下一页;
		endwhile (false)
}
stop

@enduml
