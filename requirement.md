# 線上課程報名與管理系統 - 需求概述

## 1. 系統簡介
本系統旨在模擬一個簡易的線上課程報名與管理平台。用戶可以瀏覽現有課程、報名課程、查詢自己的報名紀錄以及取消已報名的課程。
管理員可以新增、修改、刪除課程，並進行講師的排程與分配。

## 2. 功能模組與 API 端點

### 2.1 課程管理 (Course Management)
提供管理員對課程進行增、刪、改、查的操作。

* **新增課程 (Add Course)**
    * 功能描述：管理員新增一門新的課程。
    * API 端點：`POST /courses`
* **修改課程資訊 (Update Course Information)**
    * 功能描述：管理員修改現有課程的名稱、描述、最大報名人數或狀態。
    * API 端點：`PUT /courses/{courseId}`
* **刪除課程 (Delete Course)**
    * 功能描述：管理員刪除一門課程。如果課程已有報名，則不允許刪除。
    * API 端點：`DELETE /courses/{courseId}`
* **查詢所有課程 (Get All Courses)**
    * 功能描述：查詢所有可供報名的課程列表。
    * API 端點：`GET /courses`
* **查詢單一課程詳情 (Get Course Details)**
    * 功能描述：查詢指定課程的詳細資訊，包含已報名人數。
    * API 端點：`GET /courses/{courseId}`

### 2.2 課程報名與查詢 (Course Enrollment and Inquiry)
提供用戶進行課程的報名、查詢及取消。

* **報名課程 (Enroll Course)**
    * 功能描述：用戶報名指定的課程。需要檢查課程是否已滿、是否已報名過。
    * API 端點：`POST /enrollments`
* **取消報名 (Cancel Enrollment)**
    * 功能描述：用戶取消已報名的課程。
    * API 端點：`DELETE /enrollments/{enrollmentId}`
* **查詢用戶報名紀錄 (Get User Enrollments)**
    * 功能描述：查詢指定用戶的所有報名紀錄。
    * API 端點：`GET /users/{userId}/enrollments`

### 2.3 講師排程與分配 (Instructor Scheduling and Assignment) - 複雜邏輯
提供管理員進行講師的排程和課程分配，並確保講師在指定時間段內沒有衝突。

* **分配講師 (Assign Instructor)**
    * 功能描述：為指定的課程分配講師，並檢查講師在該課程時間段內是否有其他課程衝突。
        * **複雜度要求：程式碼的 Cyclomatic Complexity >= 8**
            * 需檢查：
                1.  課程是否存在。
                2.  講師是否存在。
                3.  課程時間是否與講師已分配的其他課程時間重疊。
                4.  如果時間重疊，需要判斷重疊的課程是否可以調整（例如，是否有備用講師，或者是否可以自動尋找下一個可用的時間段）。
                5.  分配成功後，更新講師的排程狀態。
                6.  分配失敗，返回詳細錯誤信息。
    * API 端點：`POST /courses/{courseId}/assignInstructor`