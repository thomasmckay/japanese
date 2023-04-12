package main

import (
	"testing"
)

func TestJapanese(t *testing.T) {
	expected := "japanese"
	if actual := Japanese(); actual != expected {
		t.Errorf("Expected %s but got %s", expected, actual)
	}
}
