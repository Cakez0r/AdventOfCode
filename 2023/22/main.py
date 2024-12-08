from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


class Point:
    x: int
    y: int
    z: int

    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def add(self, x: int, y: int, z: int):
        return Point(self.x + x, self.y + y, self.z + z)
    
    def __str__(self):
        return f"({self.x},{self.y},{self.z})"
        
class BoundingBox:
    p1: Point
    p2: Point

    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2
    
    def w(self) -> int:
        return self.p2.x - self.p1.x
    
    def h(self) -> int:
        return self.p2.y - self.p1.y

    def d(self) -> int:
        return self.p2.z - self.p1.z

    def points(self) -> list[Point]:
        return [
            self.p1,
            self.p1.add(self.w(), 0, 0),
            self.p1.add(0, self.h(), 0),
            self.p1.add(self.w(), self.h(), 0),
            self.p1.add(self.w(), 0, self.d()),
            self.p1.add(0, self.h(), self.d()),
            self.p1.add(0, 0, self.d()),
            self.p2
        ]
    
    def down(self):
        return BoundingBox(Point(self.p1.x, self.p1.y, self.p1.z - 1), Point(self.p2.x, self.p2.y, self.p2.z - 1))

    def p_intersects(self, p: Point) -> bool:
       return p.x > self.p1.x and p.x < self.p2.x and \
            p.y > self.p1.y and p.y < self.p2.y and \
            p.z >= self.p1.z and p.z <= self.p2.z
    
    def bb_intersects(self, bb: "BoundingBox") -> bool:
        return self.p1.x < bb.p2.x and bb.p1.x < self.p2.x and \
            self.p1.y < bb.p2.y and bb.p1.y < self.p2.y and \
            self.p1.z < bb.p2.z and bb.p1.z < self.p2.z
          
def can_move_down(idx:int, bricks: list[BoundingBox]) -> bool:
    b: BoundingBox = bricks[idx].down()
    if b.p1.z < 0:
        return False
    
    for i in range(len(bricks)):
        if i == idx:
            continue
        
        if b.bb_intersects(bricks[i]):
            return False

    return True

def step(bricks: list[BoundingBox]) -> tuple[int, list[BoundingBox]]:
    new_bricks = []
    changes = 0
    for i in range(len(bricks)):
        b = bricks[i]
        if can_move_down(i, bricks):
            new_bricks.append(b.down())
            changes += 1
        else:
            new_bricks.append(b)

    return changes, new_bricks

def will_move(bricks: list[BoundingBox]) -> bool:
    for i in range(len(bricks)):
        if can_move_down(i, bricks):
            return True

    return False

def count_moves(bricks: list[BoundingBox]) -> int:
    fell = set()

    changes = -1
    while changes != 0:
        new_bricks = []
        changes = 0
        for i in range(len(bricks)):
            if can_move_down(i, bricks):
                changes += 1
                new_bricks.append(bricks[i].down())
                fell.add(i)
            else:
                new_bricks.append(bricks[i])
        bricks = new_bricks
    print(len(fell))
    return len(fell)


with open("input.txt") as f:
    bricks = []
    lines = [l.strip() for l in f.readlines()]

    for l in lines:
        p1, p2 = l.split('~')
        x1,y1,z1 = [int(n) for n in p1.split(',')]
        z1 -= 1
        x2,y2,z2 = [int(n)+1 for n in p2.split(',')]
        z2 -= 1
        bricks.append(BoundingBox(Point(x1,y1,z1), Point(x2,y2,z2)))

    changes = -1
    while changes != 0:
        changes, new_bricks = step(bricks)
        bricks = new_bricks
        # print(bricks[2].p1, bricks[2].p2)
        print("Changes ", changes)

    # assert bricks[0].p1.z == 0 and bricks[0].p2.z == 1
    # assert bricks[1].p1.z == 1 and bricks[1].p2.z == 2
    # assert bricks[2].p1.z == 1 and bricks[2].p2.z == 2
    # assert bricks[3].p1.z == 2 and bricks[3].p2.z == 3
    # assert bricks[4].p1.z == 2 and bricks[4].p2.z == 3
    # assert bricks[5].p1.z == 3 and bricks[5].p2.z == 4
    # assert bricks[6].p1.z == 4 and bricks[6].p2.z == 6

    removable = 0
    blist = []
    for i in range(len(bricks)):
        blist.append(bricks[:i] + bricks[i+1:])
            
    with ThreadPoolExecutor() as p:
        result = list(p.map(count_moves, blist))
        
    print(sum(result))