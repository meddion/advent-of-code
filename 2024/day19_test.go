package advent_test

import (
	"fmt"
	"slices"
	"strings"
	"testing"
	"time"
)

func part1(data string) int {
	data = strings.TrimSpace(data)
	rows := strings.Split(data, "\n")
	combs := strings.Split(rows[0], ", ")

	var checkSeq func(seq string) bool
	checkSeq = func(seq string) bool {
		if len(seq) == 0 {
			return true
		}

		for _, comb := range combs {
			n := len(comb)
			if len(seq) >= n && seq[:n] == comb {
				if checkSeq(seq[n:]) {
					return true
				}
			}
		}

		return false
	}

	count := 0
	for _, seq := range rows[2:] {
		seq = strings.TrimSpace(seq)
		if checkSeq(seq) {
			count++
		}
	}

	return count
}

func part2(data string) int {
	data = strings.TrimSpace(data)
	rows := strings.Split(data, "\n")
	combs := strings.Split(rows[0], ", ")
	slices.SortFunc(combs, func(a, b string) int {
		if len(a) == len(b) {
			return 0
		}
		if len(a) > len(b) {
			return 1
		}
		return -1
	})

	cache := make(map[string]int)

	var checkSeq func(seq string) int
	checkSeq = func(seq string) int {
		if v, ok := cache[seq]; ok {
			return v
		}

		if len(seq) == 0 {
			return 1
		}

		count := 0
		for _, comb := range combs {
			n := len(comb)
			if len(seq) < n {
				break
			}

			if seq[:n] == comb {
				count += checkSeq(seq[n:])
			}
		}

		cache[seq] = count

		return count
	}

	sum := 0
	t0 := time.Now()
	for _, seq := range rows[2:] {
		seq = strings.TrimSpace(seq)
		sum += checkSeq(seq)
		fmt.Printf("Checked %q: %s\n", seq, time.Since(t0))
	}

	return sum

}

func TestDay19(t *testing.T) {
	testData := `
		r, wr, b, g, bwu, rb, gb, br

		brwrr
		bggr
		gbbr
		rrbgbr
		ubwu
		bwurrg
		brgr
		bbrgwb
		`
	finalData := readFile("day19.txt")
	t.Run("part1", func(t *testing.T) {
		if res := part1(testData); res != 6 {
			t.Fatalf("exp: %v, got %v: ", 6, res)
		}

		t.Log(part1(finalData))
	})

	t.Run("part2", func(t *testing.T) {
		if res := part2(testData); res != 16 {
			t.Fatalf("exp: %v, got %v: ", 16, res)
		}

		t.Log(part2(finalData))
	})
}
