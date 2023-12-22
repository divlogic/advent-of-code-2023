from .utils import Group, Node, NodeWalker, find_answer


def test_node_init():
    line = "AAA = (BBB, CCC)\n"
    node = Node(line)

    expected_point = "AAA"
    expected_left = "BBB"
    expected_right = "CCC"
    expected_options = ("BBB", "CCC")

    assert expected_point == node.point
    assert expected_left == node.left()
    assert expected_right == node.right()
    assert expected_options == node.options


def test_node_walker_init():
    expected_path = "RL"
    expected_position = 0
    expected_current = "AAA"
    expected_steps = 0
    line = "AAA = (BBB, CCC)\n"
    node = Node(line)
    node_walker = NodeWalker(expected_path, expected_current, {"AAA": node})

    assert expected_path == node_walker.path
    assert expected_position == node_walker.position
    assert expected_steps == node_walker.steps
    assert expected_current == node_walker.current


def test_node_walker_next():
    expected_path = "RL"
    expected_position = 1
    expected_current = "CCC"
    expected_steps = 1
    line_1 = "AAA = (BBB, CCC)\n"
    line_2 = "CCC = (ZZZ, GGG)"
    node_1 = Node(line_1)
    node_2 = Node(line_2)
    node_walker = NodeWalker(expected_path, "AAA", {"AAA": node_1, "CCC": node_2})

    node_walker.next()

    assert expected_path == node_walker.path
    assert expected_position == node_walker.position
    assert expected_steps == node_walker.steps
    assert expected_current == node_walker.current


def test_node_walker_next_beyond_loop():
    expected_path = "RL"
    expected_position = 1
    expected_current = "ZZZ"
    expected_steps = 3
    line_1 = "AAA = (BBB, CCC)\n"
    line_2 = "CCC = (ZZZ, GGG)\n"
    line_3 = "ZZZ = (ZZZ, ZZZ)\n"
    node_1 = Node(line_1)
    node_2 = Node(line_2)
    node_3 = Node(line_3)
    node_walker = NodeWalker(
        expected_path, "AAA", {"AAA": node_1, "CCC": node_2, "ZZZ": node_3}
    )

    node_walker.next()
    node_walker.next()
    node_walker.next()

    assert expected_path == node_walker.path
    assert expected_position == node_walker.position
    assert expected_steps == node_walker.steps
    assert expected_current == node_walker.current


def test_group_init():
    line_1 = "11A = (11B, XXX)"
    line_2 = "11B = (XXX, 11Z)"
    line_3 = "11Z = (11B, XXX)"
    line_4 = "22A = (22B, XXX)"

    node_1 = Node(line_1)
    node_2 = Node(line_2)
    node_3 = Node(line_3)
    node_4 = Node(line_4)

    node_walker_1 = NodeWalker(
        "LR", "11A", {"11A": node_1, "11B": node_2, "11Z": node_3, "22A": node_4}
    )
    node_walker_2 = NodeWalker(
        "LR", "22A", {"11A": node_1, "11B": node_2, "11Z": node_3, "22A": node_4}
    )
    group = Group([node_walker_1, node_walker_2])

    expected_container = [node_walker_1, node_walker_2]

    assert expected_container == group.container


def test_group_arrived_false():
    line_1 = "11A = (11B, XXX)"
    line_2 = "11B = (XXX, 11Z)"
    line_3 = "11Z = (11B, XXX)"
    line_4 = "22A = (22B, XXX)"

    node_1 = Node(line_1)
    node_2 = Node(line_2)
    node_3 = Node(line_3)
    node_4 = Node(line_4)

    node_walker_1 = NodeWalker(
        "LR", "11A", {"11A": node_1, "11B": node_2, "11Z": node_3, "22A": node_4}
    )
    node_walker_2 = NodeWalker(
        "LR", "22A", {"11A": node_1, "11B": node_2, "11Z": node_3, "22A": node_4}
    )
    group = Group([node_walker_1, node_walker_2])

    expected_answer = False

    assert expected_answer == group.arrived()


def test_group_arrived_true():
    line_1 = "11A = (11B, XXX)"
    line_2 = "11B = (XXX, 11Z)"
    line_3 = "11Z = (11B, XXX)"
    line_4 = "22A = (22B, XXX)"
    line_5 = "22Z = (22B, 22B)"

    node_1 = Node(line_1)
    node_2 = Node(line_2)
    node_3 = Node(line_3)
    node_4 = Node(line_4)
    node_5 = Node(line_5)

    node_walker_1 = NodeWalker(
        "LR",
        "11Z",
        {"11A": node_1, "11B": node_2, "11Z": node_3, "22A": node_4, "22Z": node_5},
    )
    node_walker_2 = NodeWalker(
        "LR",
        "22Z",
        {"11A": node_1, "11B": node_2, "11Z": node_3, "22A": node_4, "22Z": node_5},
    )
    group = Group([node_walker_1, node_walker_2])

    expected_answer = True

    assert expected_answer == group.arrived()


def test_find_answer():
    expected = 6
    actual = find_answer("input.test.txt")
    assert expected == actual
