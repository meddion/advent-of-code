package advent_test

import (
	"fmt"
	"io"
	. "math"
	"os"
	"strconv"
	"strings"
	"testing"
)

var steps = []XY{{0, -1}, {-1, 0}, {1, 0}, {0, 1}}

type XY struct {
	x, y int
}

func readFile(fileName string) string {
	file, err := os.Open(fileName)
	noError(err)

	data, err := io.ReadAll(file)
	noError(err)

	return string(data)
}

func parseObstacles(positionsStr string, cap int) (map[XY]struct{}, []XY) {
	rows := strings.Split(positionsStr, "\n")
	positionsSet := make(map[XY]struct{}, len(rows))

	parseRow := func(row string) *XY {
		row = strings.TrimSpace(row)
		if row == "" {
			return nil
		}

		i := strings.Index(row, ",")
		num1, err := strconv.Atoi(row[:i])
		noError(err)
		num2, err := strconv.Atoi(row[i+1:])
		noError(err)

		return &XY{x: num1, y: num2}
	}

	for _, row := range rows[:cap] {
		pos := parseRow(row)
		if pos == nil {
			continue
		}

		positionsSet[*pos] = struct{}{}
	}

	restBytes := make([]XY, len(rows)-cap)
	for i, row := range rows[cap:] {
		pos := parseRow(row)

		if pos == nil {
			continue
		}
		restBytes[i] = *pos
	}

	return positionsSet, restBytes
}

func shortestPath(obstacleSet map[XY]struct{}, endX, endY int) int {
	visited := make(map[XY]struct{})
	visited[XY{}] = struct{}{}

	type item struct {
		XY
		length int
	}
	posQueue := []item{{}}

	minLen := MaxInt64

	for len(posQueue) > 0 {
		pos := posQueue[0]
		posQueue = posQueue[1:]

		if pos.x == endX && pos.y == endY {
			minLen = min(minLen, pos.length)
			continue
		}

		for _, step := range steps {
			newPos := item{}
			newPos.x = pos.x + step.x
			newPos.y = pos.y + step.y
			newPos.length = pos.length + 1

			_, isObstacle := obstacleSet[newPos.XY]
			_, isVisited := visited[newPos.XY]
			if isObstacle || isVisited || newPos.x < 0 || newPos.x > endX || newPos.y < 0 || newPos.y > endY {
				continue
			}

			visited[newPos.XY] = struct{}{}
			posQueue = append(posQueue, newPos)
		}

	}

	return minLen
}

func firstByteToBlockExit(obstacleSet map[XY]struct{}, restObst []XY, endX, endY int) XY {
	for _, obst := range restObst {
		obstacleSet[obst] = struct{}{}

		if shortestPath(obstacleSet, endX, endY) == MaxInt64 {
			return obst
		}

		// delete(obstacleSet, obst)
	}

	return XY{}
}

func TestDay18(t *testing.T) {
	obstacles := readFile("day18.txt")
	obstacleSet, restObst := parseObstacles(obstacles, 1024)
	t.Run("part_1", func(t *testing.T) {
		t.Log(shortestPath(obstacleSet, 70, 70))
	})

	t.Run("part_2", func(t *testing.T) {
		fmt.Printf("Answer: %#v", firstByteToBlockExit(obstacleSet, restObst, 70, 70))

		data := `
			5,4
			4,2
			4,5
			3,0
			2,1
			6,3
			2,4
			1,5
			0,6
			3,3
			2,6
			5,1
			1,2
			5,5
			2,5
			6,5
			1,4
			0,4
			6,4
			1,1
			6,1
			1,0
			0,5
			1,6
			2,0`

		exp := XY{x: 6, y: 1}
		obsSet, restObst := parseObstacles(data, 12)
		if got := firstByteToBlockExit(obsSet, restObst, 6, 6); got != exp {
			t.Fatalf("exp: %#v, got: %#v", exp, got)
		}
	})
}
