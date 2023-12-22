from .utils import Node, NodeNetwork, find_answer


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


def test_node_network_init():
    expected_path = "RL"
    expected_position = 0
    expected_current = "AAA"
    expected_steps = 0
    line = "AAA = (BBB, CCC)\n"
    node = Node(line)
    node_network = NodeNetwork(expected_path, expected_current, {"AAA": node})

    assert expected_path == node_network.path
    assert expected_position == node_network.position
    assert expected_steps == node_network.steps
    assert expected_current == node_network.current


def test_node_network_next():
    expected_path = "RL"
    expected_position = 1
    expected_current = "CCC"
    expected_steps = 1
    line_1 = "AAA = (BBB, CCC)\n"
    line_2 = "CCC = (ZZZ, GGG)"
    node_1 = Node(line_1)
    node_2 = Node(line_2)
    node_network = NodeNetwork(expected_path, "AAA", {"AAA": node_1, "CCC": node_2})

    node_network.next()

    assert expected_path == node_network.path
    assert expected_position == node_network.position
    assert expected_steps == node_network.steps
    assert expected_current == node_network.current


def test_node_network_next_beyond_loop():
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
    node_network = NodeNetwork(
        expected_path, "AAA", {"AAA": node_1, "CCC": node_2, "ZZZ": node_3}
    )

    node_network.next()
    node_network.next()
    node_network.next()

    assert expected_path == node_network.path
    assert expected_position == node_network.position
    assert expected_steps == node_network.steps
    assert expected_current == node_network.current


def test_find_answer():
    expected = 2
    actual = find_answer("input.test.txt")
    assert expected == actual


def test_find_answer_2():
    expected = 6
    actual = find_answer("input_2.test.txt")
    assert expected == actual
