package advent_test

import (
	"fmt"
	. "math"
	"regexp"
	"strconv"
	"strings"
	"testing"

	"slices"
)

const (
	ADV = iota
	BXL
	BST
	JNZ
	BXC
	OUT
	BDV
	CDV
)

func noError(err error) {
	if err != nil {
		panic(err)
	}
}

func initRegisters(progStr string) registers {
	var registerReg = regexp.MustCompile("Register (A|B|C): (\\d+)")

	var err error
	var a, b, c int
	for _, res := range registerReg.FindAllStringSubmatch(progStr, -1) {
		switch res[1] {
		case "A":
			a, err = strconv.Atoi(res[2])
		case "B":
			b, err = strconv.Atoi(res[2])
		default:
			c, err = strconv.Atoi(res[2])
		}

		noError(err)
	}

	return registers{A: a, B: b, C: c}
}

func programSeq(progStr string) (program []int, programStr string) {
	var programReg = regexp.MustCompile(`Program: ([\d,]+)`)
	matches := programReg.FindStringSubmatch(progStr)

	for _, op := range strings.Split(matches[1], ",") {
		num, err := strconv.Atoi(op)
		noError(err)
		program = append(program, num)
	}

	return program, matches[1]
}

func combOperandValue(regs registers, operand int) int {
	if operand < 0 || operand >= 7 {
		panic("not valid operand")
	}

	if operand < 4 {
		return operand
	}

	switch operand {
	case 4:
		return regs.A
	case 5:
		return regs.B
	}

	return regs.C
}

type registers struct {
	A, B, C int
}

func runProgramPart1(progStr string) string {
	regs := initRegisters(progStr)
	program, _ := programSeq(progStr)

	outputs := make([]string, 0)
	i := 0
	for i < len(program) {
		opCode := program[i]

		switch opCode {
		case ADV:
			operand := combOperandValue(regs, program[i+1])
			regs.A /= int(Pow(2.0, float64(operand)))
		case BDV:
			operand := combOperandValue(regs, program[i+1])
			regs.B = regs.A / int(Pow(2.0, float64(operand)))
		case CDV:
			operand := combOperandValue(regs, program[i+1])
			regs.C = regs.A / int(Pow(2.0, float64(operand)))
		case BXL:
			regs.B ^= program[i+1]
		case BXC:
			regs.B ^= regs.C
		case BST:
			operand := combOperandValue(regs, program[i+1])
			regs.B = operand % 8
		case OUT:
			operand := combOperandValue(regs, program[i+1])
			outputs = append(outputs, strconv.Itoa(operand%8))
		case JNZ:
			if regs.A != 0 {
				i = program[i+1] - 2
			}

		}

		i += 2
	}

	return strings.Join(outputs, ",")
}

func TestPart1Test1(t *testing.T) {
	program := `
		Register A: 729
		Register B: 0
		Register C: 0

		Program: 0,1,5,4,3,0
	`

	if res := runProgramPart1(program); res != "4,6,3,5,6,3,5,2,1,0" {
		t.Errorf("Got %q as output instead", res)
	}

	finalProgram := `
		Register A: 61657405
		Register B: 0
		Register C: 0

		Program: 2,4,1,2,7,5,4,3,0,3,1,7,5,5,3,0
	`

	t.Log(runProgramPart1(finalProgram))
}

func runProgramPart2(progAndData string) int {
	regs := registers{}
	program, _ := programSeq(progAndData)

	runProgram := func(A int, program []int) []int {
		regs.A = A
		outputs := make([]int, 0)
		i := 0
		for i < len(program) {
			opCode := program[i]

			switch opCode {
			case ADV:
				operand := combOperandValue(regs, program[i+1])
				regs.A = regs.A / int(Pow(2.0, float64(operand)))
			case BDV:
				operand := combOperandValue(regs, program[i+1])
				regs.B = regs.A / int(Pow(2.0, float64(operand)))
			case CDV:
				operand := combOperandValue(regs, program[i+1])
				regs.C = regs.A / int(Pow(2.0, float64(operand)))
			case BXL:
				regs.B = regs.B ^ program[i+1]
			case BXC:
				regs.B ^= regs.C
			case BST:
				operand := combOperandValue(regs, program[i+1])
				regs.B = operand % 8
			case OUT:
				operand := combOperandValue(regs, program[i+1])
				outputs = append(outputs, operand%8)
			case JNZ:
				if regs.A != 0 {
					i = program[i+1] - 2
				}

			}

			i += 2
		}

		return outputs
	}

	slices.Reverse(program)

	type item struct {
		A   int
		idx int
	}
	possibleAs := []item{{A: 0, idx: 0}}

	for len(possibleAs) > 0 {
		it := possibleAs[0]
		possibleAs = possibleAs[1:]
		A, idx := it.A, it.idx
		if idx == len(program) {
			return A
		}

		for i := range 8 {
			A_next := (A << 3) + i

			out := runProgram(A_next, program[:idx+1])
			if slices.Equal(out, program[:idx+1]) {
				possibleAs = append(possibleAs, item{A: A_next, idx: idx + 1})
			}

		}
	}

	return -1
}

func printProgram(progAndData string) {
	program, programStr := programSeq(progAndData)

	combOperand := func(operand int) string {
		if operand < 0 || operand >= 7 {
			panic("not valid operand")
		}

		if operand < 4 {
			return strconv.Itoa(operand)
		}

		switch operand {
		case 4:
			return "A"
		case 5:
			return "B"
		}

		return "C"
	}

	fmt.Printf("Program: %s\n", programStr)

	i := 0
	for i < len(program) {
		op := "undef"
		operand := "_"
		details := ""

		switch program[i] {
		case ADV:
			op = "adv"
			operand = combOperand(program[i+1])
			details = fmt.Sprintf("A = A / 2**%s", operand)
		case BDV:
			op = "bdv"
			operand = combOperand(program[i+1])
			details = fmt.Sprintf("B = A / 2**%s", operand)
		case CDV:
			op = "cdv"
			operand = combOperand(program[i+1])
			details = fmt.Sprintf("C = A / 2**%s", operand)
		case BXL:
			op = "bxl"
			operand = strconv.Itoa(program[i+1])
			details = fmt.Sprintf("B ^= %s", operand)
		case BXC:
			op = "bxc"
			details = "B ^= C"
		case BST:
			op = "bst"
			operand = combOperand(program[i+1])
			details = fmt.Sprintf("B = %s %% 8", operand)
		case OUT:
			op = "out"
			operand = combOperand(program[i+1])
			details = fmt.Sprintf("print(%s %% 8)", operand)
		case JNZ:
			op = "jnz"
			operand = combOperand(program[i+1])
			details = fmt.Sprintf("if A != 0: jump %s", operand)
		}

		fmt.Printf("%d:%d\t%s %s\t# %s\n", i, i+1, op, operand, details)
		i += 2
	}
}

func TestPart2Test1(t *testing.T) {
	finalProgram := `
		Register A: 61657405
		Register B: 0
		Register C: 0

		Program: 2,4,1,2,7,5,4,3,0,3,1,7,5,5,3,0
	`
	// printProgram(finalProgram)
	t.Log(runProgramPart2(finalProgram))
}
