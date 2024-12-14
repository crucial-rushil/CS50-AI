# Analysis

## Layer 4, Head 10
In this layer, I noticed that this attention head is paying attention to all noun phrases in the sentence.
A noun phrase can be defined as a delimiter or possesive pronoun followed by a noun or just a noun. This is evidenced by I love walking my [MASK] at the park. The head correctly identifies "I love" (love can be a noun), "my [MASK] (found to be dog)", "at park", "the park". It also pays attention to individual Nouns and CLS and SEP.

Example Sentences:
- I love walking my [MASK] at the park
- I like riding my [MASK] around the neighborhood

## Layer 3, Head 1

In this layer, the attention head appears to be paying attention to words that immediately follow a current word in the sentence. This is shown by one large diagnoal of all whites and the SEP is followed by CLS. It appears to be trying to establish an order of the words.

Example Sentences:
- I love walking my [MASK] at the park
- I like riding my [MASK] around the neighborhood

