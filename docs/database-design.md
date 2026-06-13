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
