package advent_test

import (
	"strings"
	"testing"
)

func countCheats(data string) int {
	data = strings.TrimSpace(data)
	var arena [][]byte
	var start, end XY
	for i, row := range strings.Split(data, "\n") {
		row = strings.TrimSpace(row)
		byteRow := []byte(row)
		for j, b := range byteRow {
			switch b {
			case 'S':
				start = XY{x: j, y: i}
			case 'E':
				end = XY{x: j, y: i}
			}
		}

		arena = append(arena, byteRow)
	}

	visited := make(map[XY]struct{})
	cheats := make(map[int]int)
	// Pre-allocate to reduce allocations father
	cache := make(map[XY]int, len(arena)*len(arena[0])/2)
	type item struct {
		XY
		track   []XY
		isCheat bool
	}
	queue := []item{{XY: start}}

	for len(queue) > 0 {
		curItem := queue[len(queue)-1]
		queue = queue[:len(queue)-1]

		if trackLen, ok := cache[curItem.XY]; ok {
			n := len(curItem.track) + trackLen
			for i, xy := range curItem.track {
				cache[xy] = n - i
			}

			if curItem.isCheat {
				cheats[n]++
			}

			continue
		}

		if curItem.XY == end {
			n := len(curItem.track)
			for i, xy := range curItem.track {
				cache[xy] = n - i
			}

			if curItem.isCheat {
				cheats[n]++
			}

			continue
		}

		for _, step := range steps {
			it := item{}
			it.x = curItem.x + step.x
			it.y = curItem.y + step.y

			if it.x < 0 || it.x > len(arena[0]) || it.y < 0 || it.y >= len(arena) {
				continue
			}

			if arena[it.y][it.x] == '#' && !curItem.isCheat {
				it.isCheat = true
				it.track = append(curItem.track, curItem.XY)
			}

			if arena[it.y][it.x] == '.' {
				it.track = append(curItem.track, curItem.XY)
			}
		}
	}

	return 0
}

func TestDay20(t *testing.T) {
	t.Run("part_1", func(t *testing.T) {
		data := `
		###############
		#...#...#.....#
		#.#.#.#.#.###.#
		#S#...#.#.#...#
		#######.#.#.###
		#######.#.#...#
		#######.#.###.#
		###..E#...#...#
		###.#######.###
		#...###...#...#
		#.#####.#.###.#
		#.#...#.#.#...#
		#.#.#.#.#.#.###
		#...#...#...###
		###############
	 	`

		res := countCheats(data)
		t.Log(res)

	})
}
