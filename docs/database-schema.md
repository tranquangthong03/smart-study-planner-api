# Mô tả bảng chi tiết để chuẩn bị cho code
## Relationship Rules

### User and StudyGoal

Một user có thể có nhiều study goals.

Nếu xóa user, có thể xóa toàn bộ goals liên quan.

Quan hệ:

users.id -> study_goals.user_id

### StudyGoal and Topic

Một study goal có thể có nhiều topics.

Nếu xóa goal, có thể xóa toàn bộ topics thuộc goal.

Quan hệ:

study_goals.id -> topics.goal_id

### Topic and StudyTask

Một topic có thể có nhiều study tasks.

Nếu xóa topic, có thể xóa toàn bộ tasks thuộc topic.

Quan hệ:

topics.id -> study_tasks.topic_id

### StudyTask and StudySession

Một task có thể có nhiều study sessions.

Nếu xóa task, có thể xóa toàn bộ study sessions thuộc task.

Quan hệ:

study_tasks.id -> study_sessions.task_id

### StudyTask and ReviewSchedule

Một task có thể có nhiều review schedules.

Nếu xóa task, có thể xóa toàn bộ review schedules thuộc task.

Quan hệ:

study_tasks.id -> review_schedules.task_id
## Delete Rules

### User

Không xóa thật user trong MVP.

Nếu cần khóa tài khoản, cập nhật:

is_active = false

### StudyGoal

Khi xóa goal, các topic thuộc goal cũng nên bị xóa.

### Topic

Khi xóa topic, các task thuộc topic cũng nên bị xóa.

### StudyTask

Khi xóa task, các study sessions và review schedules thuộc task cũng nên bị xóa.

### StudySession

Có thể xóa trực tiếp.

### ReviewSchedule

Có thể xóa trực tiếp.
## Status Values

### study_goals.status

| Value | Meaning |
|---|---|
| active | Đang học |
| completed | Đã hoàn thành |
| paused | Tạm dừng |
| cancelled | Đã hủy |

### topics.status

| Value | Meaning |
|---|---|
| not_started | Chưa bắt đầu |
| in_progress | Đang học |
| completed | Đã hoàn thành |

### study_tasks.status

| Value | Meaning |
|---|---|
| pending | Chưa làm |
| in_progress | Đang làm |
| completed | Đã hoàn thành |
| skipped | Bỏ qua |

### review_schedules.status

| Value | Meaning |
|---|---|
| pending | Chưa ôn |
| completed | Đã ôn |
| missed | Bỏ lỡ |
## Index Plan

### users

| Column | Reason |
|---|---|
| email | Tìm user khi login |

### study_goals

| Column | Reason |
|---|---|
| user_id | Lấy goals theo user |
| status | Lọc goals theo trạng thái |

### topics

| Column | Reason |
|---|---|
| goal_id | Lấy topics theo goal |
| status | Lọc topics theo trạng thái |

### study_tasks

| Column | Reason |
|---|---|
| topic_id | Lấy tasks theo topic |
| due_date | Lấy task hôm nay |
| status | Lọc task theo trạng thái |

### study_sessions

| Column | Reason |
|---|---|
| task_id | Lấy sessions theo task |
| started_at | Thống kê theo thời gian học |

### review_schedules

| Column | Reason |
|---|---|
| task_id | Lấy reviews theo task |
| review_date | Lấy reviews hôm nay |
| status | Lọc reviews theo trạng thái |