package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"os/exec"
	"regexp"
	"strings"
	"time"
)

type Word struct {
	english  string
	japanese string
}

type Category interface {
	Name() string
	English() string
	Japanese() string
	Populate(args ...Word) bool
}

type SubjectIsAdjectiveCategory struct {
	english  string
	japanese string

	subject   Word
	adjective Word
}

func (c *SubjectIsAdjectiveCategory) Name() string {
	return "SUBJECT IS ADJECTIVE"
}

func (c *SubjectIsAdjectiveCategory) English() string {
	return c.english
}

func (c *SubjectIsAdjectiveCategory) Japanese() string {
	return c.japanese
}

func (c *SubjectIsAdjectiveCategory) Populate(args ...Word) bool {
	space := regexp.MustCompile(`\s+`)
	format := Word{
		"%s %s %s %s",
		"%s %s %s %s %s",
	}

	is_or_isnot := []Word{
		{"IS", "です"},
		{"IS NOT", "じゃないです"},
		{"IS ALSO", "です"},
		{"IS ALSO NOT", "じゃないです"},
	}
	prefix := []Word{
		{"THE", ""},
		{"THIS (NEAR ME)", "この"},
		{"THAT (NEAR YOU)", "その"},
		{"THAT (NOT NEAR)", "あの"},
	}

	c.subject = args[0]
	c.adjective = args[1]

	v := is_or_isnot[rand.Intn(len(is_or_isnot)-1)]
	p := prefix[rand.Intn(len(prefix)-1)]
	j := "は"
	if strings.Contains(v.english, "ALSO") {
		j = "も"
	}

	c.japanese = space.ReplaceAllString(fmt.Sprintf(format.japanese,
		p.japanese,
		c.subject.japanese,
		j,
		c.adjective.japanese,
		v.japanese,
	), " ")

	c.english = space.ReplaceAllString(fmt.Sprintf(format.english,
		p.english,
		c.subject.english,
		v.english,
		c.adjective.english,
	), " ")

	return true
}

type AnotherCategory struct {
	english  string
	japanese string

	something Word
}

func (c *AnotherCategory) Name() string {
	return "SOMETHING"
}

func (c *AnotherCategory) English() string {
	return c.english
}

func (c *AnotherCategory) Japanese() string {
	return c.japanese
}

func (c *AnotherCategory) Populate(args ...Word) bool {
	c.something = args[0]

	return true
}

var Nouns = []Word{
	{"APPLE", "りんご"},
}

var Adjectives = []Word{
	{"RED", "あかい"},
}

func Japanese() string {
	// fmt.Fprintf(os.Stderr, "japanese %s", os.Args[0])

	var categories = []Category{
		&SubjectIsAdjectiveCategory{
			english: "english", japanese: "japanese",
		},
		&AnotherCategory{
			english: "english something", japanese: "japanese something",
		},
	}

	reader := bufio.NewReader(os.Stdin)
	for {
		clear()
		categories[0].Populate(Nouns[0], Adjectives[0])

		fmt.Fprintf(os.Stderr, "%s\n", categories[0].English())
		if text, _ := reader.ReadString('\n'); text == "q\n" {
			break
		}
		fmt.Fprintf(os.Stderr, "%s\n", categories[0].Japanese())
		if text, _ := reader.ReadString('\n'); text == "q\n" {
			break
		}
	}

	return "japanese"
}

func clear() {
	cmd := exec.Command("clear") //Linux example, its tested
	cmd.Stdout = os.Stdout
	cmd.Run()
}

func main() {
	rand.Seed(time.Now().Unix())
	fmt.Println(Japanese())
}
