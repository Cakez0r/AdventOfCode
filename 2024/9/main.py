class File:
    id: int
    size: int
    pad: int
    next: "File"
    prev: "File"


def compact(head: File, tail: File):
    # This is so cooked...
    uncompacted_length = len(to_str(head))
    og_head = head
    while True:
        tail.prev.next = None

        f = File()
        f.id = tail.id
        f.prev = head
        f.next = head.next
        f.pad = 0

        if head.next:
            head.next.prev = f
        else:
            head.pad = tail.size

        f.size = min(tail.size, head.pad)
        
        head.next = f
        
        f.pad = max(head.pad - tail.size, 0)
        tail.size -= head.pad
        head.pad = 0

        while head.pad == 0:
            if not head.next:
                f.pad = uncompacted_length - len(to_str(og_head))
                return
            
            head = head.next
        
        while tail.size <= 0:
            tail = tail.prev

def compact2(head: File, tail: File):
    og_head = head

    while tail:
        p = og_head
        next_tail = tail.prev
        while p is not tail:
            if tail.size <= p.pad:
                tail.prev.pad += tail.size + tail.pad
                tail.prev.next = tail.next

                tail.next = p.next
                p.next.prev = tail
                p.next = tail
                tail.prev = p
                tail.pad = p.pad - tail.size
                p.pad = 0
                break
            
            p = p.next
        
        # print(to_str(og_head))

        tail = next_tail

def checksum(head: File):
    sum = 0
    i = 0
    while head:
        for _ in range(head.size):
            sum += i * head.id
            i += 1
        i += head.pad
        head = head.next

    return sum


def to_str(head: File):
    s = ''
    while head:
        for _ in range(head.size):
           s += str(head.id)
        
        for _ in range(head.pad):
            s += '.'

        head = head.next

    return s


with open("input.txt") as f:
    input = f.read() + '0'
    input = input.strip()
    head = None
    tail = None
    for i in range(0, len(input), 2):
        f = File()
        f.size = int(input[i])
        f.pad = int(input[i+1])
        f.id = int(i / 2)
        f.prev = tail
        f.next = None

        if tail:
            tail.next = f

        tail = f

        if head == None:
            head = f 
    
    print(to_str(head))
    # assert to_str(head) == '00...111...2...333.44.5555.6666.777.888899'
    compact2(head, tail)
    s = to_str(head)
    print(s)
    # assert to_str(head) == '0099811188827773336446555566..............'
    cs = checksum(head)
    print(cs)
