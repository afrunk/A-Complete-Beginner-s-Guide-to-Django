- master - 没有表单的前端布局样式，已配置好路由和跳转，可以用来迁移其他主题
- formSelf - 在 master 基础上未使用 Form API 添加了表单功能
- FormAPI - 在 master 基础上使用 Form API 添加了表单功能
- auth - 在 FormAPI 基础上添加了用户注册、登录、注销、重置密码、忘记密码等完整的用户功能
- reply_list 回复列表，限制未登录用户无法回复，使用 QuerySet 操作数据库查询得到阅读数、回复数、最近回复链接
- Finaly 实现视图的优化 剩余分页、支持makedown\用户页未实现