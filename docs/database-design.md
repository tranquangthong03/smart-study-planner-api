## Main Entities
### 1. User
Đại diện cho người dùng của hệ thống.
Một user có thể tạo nhiều mục tiêu học tập.

### 2. StudyGoal
Đại diện cho 1 mục tiêu học tập lớn.
Ví dụ:
- Học FastAPI trong 30 ngày
- Ôn DSA trong 3 tháng
- Học SQL cơ bản
### 3. Topic
Đại diện cho 1 chủ đề nhỏ nằm trong mục tiêu học tập.
Ví dụ goal "Học FastAPI" có thể có các topic:
- Routing
- Pydantic
- SQLAlchemy
- JWT Authentication
### 4. StudyTask
Đại diện cho một việc học cụ thể cần làm.

Ví dụ:
- Đọc tài liệu về SQLAlchemy
- Làm bài tập CRUD User
- Ôn lại JWT Authentication

### 5. StudySession

Đại diện cho một phiên học thực tế của người dùng.

Ví dụ:
- Học FastAPI từ 19:00 đến 20:30
- Làm 2 bài DSA trong 45 phút

### 6. ReviewSchedule

Đại diện cho lịch ôn tập lại kiến thức.

## Entity Relationships

### User - StudyGoal

User 1 - n StudyGoal

Một user có thể có nhiều study goals.

### StudyGoal - Topic

Một study goal có thể gồm nhiều topic.

Quan hệ:

StudyGoal 1 - n Topic
### Topic - StudyTask

Một topic có thể có nhiều task học tập.

Quan hệ:

Topic 1 - n StudyTask
### StudyTask - StudySession

Một task có thể được thực hiện qua nhiều phiên học.

Quan hệ:

StudyTask 1 - n StudySession
### StudyTask - ReviewSchedule

Khi task hoàn thành, hệ thống có thể tạo lịch ôn tập cho task đó.

Quan hệ:

StudyTask 1 - n ReviewSchedule
## Status Definitions

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
## Main Business Flows

### Flow 1: Register and Login

1. User đăng ký bằng email và password.
2. Hệ thống kiểm tra email đã tồn tại chưa.
3. Hệ thống hash password.
4. Hệ thống lưu user vào database.
5. User đăng nhập.
6. Hệ thống kiểm tra password.
7. Hệ thống trả về JWT token.

### Flow 2: Create Study Goal

1. User gửi request tạo mục tiêu học tập.
2. Hệ thống kiểm tra user đã đăng nhập.
3. Hệ thống lưu goal với user_id hiện tại.
4. Goal mới có trạng thái active.
## MVP Scope

### In Scope

- User register/login
- Create/update/delete study goals
- Create/update/delete topics
- Create/update/delete study tasks
- Mark task as completed
- Create study sessions
- Create simple review schedules
- Basic statistics

### Out of Scope

- AI/LLM integration
- Google Calendar integration
- Email notification
- Telegram notification
- Payment
- Multi-user collaboration
- Public sharing
- Mobile app

