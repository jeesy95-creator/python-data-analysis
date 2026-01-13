from collections import deque

# ============================================================
# Version 1 (원본 스타일) - ⚠️ 주의
# ------------------------------------------------------------
# - target 칸을 큐에 넣거나(통과처럼) 처리하면 논리적으로 위험해질 수 있음
# - 아래 v2/v3를 정답/권장으로 사용
# ============================================================

def solution_v1(storage, requests):
    grid = [list(row) for row in storage]
    n = len(grid)
    m = len(grid[0])

    def remove_accessible(target):
        visited = [[False] * m for _ in range(n)]
        to_remove = set()

        queue = []
        # 가장자리에서 시작 (빈 공간 OR target)
        for i in range(n):
            for j in range(m):
                if i == 0 or i == n - 1 or j == 0 or j == m - 1:
                    if grid[i][j] == '.' or grid[i][j] == target:
                        queue.append((i, j))
                        visited[i][j] = True
                        if grid[i][j] == target:
                            to_remove.add((i, j))

        idx = 0
        while idx < len(queue):
            i, j = queue[idx]
            idx += 1

            # target이면 더 진행 안 함
            if grid[i][j] == target:
                continue

            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < m and not visited[ni][nj]:
                    visited[ni][nj] = True

                    if grid[ni][nj] == '.':
                        queue.append((ni, nj))
                    elif grid[ni][nj] == target:
                        to_remove.add((ni, nj))
                        queue.append((ni, nj))  # ⚠️ target을 큐에 넣는 건 위험

        for i, j in to_remove:
            grid[i][j] = '.'

    for req in requests:
        if len(req) == 2:  # 크레인
            target = req[0]
            for i in range(n):
                for j in range(m):
                    if grid[i][j] == target:
                        grid[i][j] = '.'
        else:  # 지게차
            remove_accessible(req[0])

    return sum(grid[i][j] != '.' for i in range(n) for j in range(m))


# ============================================================
# Version 2 (수정 정답)
# ------------------------------------------------------------
# 핵심:
# - BFS는 '.'(빈 공간)만 이동
# - 인접한 target만 제거 대상으로 추가 (target 칸으로 이동 X)
# ============================================================

def solution_v2(storage, requests):
    grid = [list(row) for row in storage]
    n, m = len(grid), len(grid[0])

    def remove_accessible(target):
        visited = [[False] * m for _ in range(n)]
        to_remove = set()
        q = deque()

        # 1) 가장자리에서 '.'만 BFS 시작점
        #    가장자리 target은 즉시 접근 가능 → 제거 후보
        for i in range(n):
            for j in range(m):
                if i in (0, n - 1) or j in (0, m - 1):
                    if grid[i][j] == '.':
                        visited[i][j] = True
                        q.append((i, j))
                    elif grid[i][j] == target:
                        to_remove.add((i, j))

        # 2) 빈 칸만 이동하며 인접 target을 제거 대상으로 체크
        while q:
            i, j = q.popleft()
            for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < m and not visited[ni][nj]:
                    if grid[ni][nj] == '.':
                        visited[ni][nj] = True
                        q.append((ni, nj))
                    elif grid[ni][nj] == target:
                        to_remove.add((ni, nj))
                        # target은 통로가 아니므로 visited 처리/큐 삽입 불필요

        for i, j in to_remove:
            grid[i][j] = '.'

    # 요청 처리
    for req in requests:
        if len(req) == 2:  # 크레인
            target = req[0]
            for i in range(n):
                for j in range(m):
                    if grid[i][j] == target:
                        grid[i][j] = '.'
        else:  # 지게차
            remove_accessible(req[0])

    return sum(grid[i][j] != '.' for i in range(n) for j in range(m))


# ============================================================
# Version 3 (최종 권장) - outside 패딩 BFS
# ------------------------------------------------------------
# 아이디어:
# - 격자를 '.'로 둘러싼 (n+2)×(m+2) 패딩을 만든다.
# - (0,0)에서 BFS를 돌면 "외부 공기" 영역이 한 번에 구해진다.
# - 외부 공기와 맞닿은 target만 제거 가능(지게차)
# ============================================================

def solution(storage, requests):
    # 패딩 포함 보드 구성
    n, m = len(storage), len(storage[0])
    board = [['.'] * (m + 2) for _ in range(n + 2)]
    for i in range(n):
        for j in range(m):
            board[i + 1][j + 1] = storage[i][j]

    def forklift_remove(target):
        # 외부 공기 영역 BFS
        visited = [[False] * (m + 2) for _ in range(n + 2)]
        q = deque([(0, 0)])
        visited[0][0] = True

        to_remove = []
        while q:
            x, y = q.popleft()
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < n + 2 and 0 <= ny < m + 2 and not visited[nx][ny]:
                    if board[nx][ny] == '.':
                        visited[nx][ny] = True
                        q.append((nx, ny))
                    elif board[nx][ny] == target:
                        # 외부 공기와 인접한 target은 접근 가능 → 제거
                        to_remove.append((nx, ny))
                        # target은 통로가 아니므로 BFS 확장은 하지 않음

        for x, y in to_remove:
            board[x][y] = '.'

    def crane_remove(target):
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if board[i][j] == target:
                    board[i][j] = '.'

    for req in requests:
        target = req[0]
        if len(req) == 2:   # 크레인
            crane_remove(target)
        else:               # 지게차
            forklift_remove(target)

    # 패딩 제외하고 카운트
    remain = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if board[i][j] != '.':
                remain += 1
    return remain
