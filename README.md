
# Background

To check the effects of [Gas cost increases for state access opcodes](https://notes.ethereum.org/@vbuterin/BkrNbeAfD), 
a modified [geth-version](https://github.com/holiman/go-ethereum/tree/access_lists) with support for the to-be-eip was used.

## Setup

The experiment was run on Goerli blocks from `number=3321372` to `number=3321425`, using a fast-synced
geth with `gcmode=archive`, thus not pruning state.

A modified version of `standardTraceBlockToFile` was added to the geth instance, making it
possible to trace blocks using alternate rules, like so:

```javascript
    debug.standardTraceBlockToFile(blockhash,{"overrides":{
        "yoloV2Block": 0
        }})
```

The `analysis.js` was loaded, and the traces were generated (see `./traces/`), containing
the trace for `53` blocks, totalling `106` transactions.

## The experiment

When running with new rules, two things can typically happen:

1. The execution flow is broken. The easiest way to detect this is to compare the number of
    operations executed. If the exact same operations were executed in both traces, the flow was not broken.
2. The execution flow was not broken.

For 1), it is interesting to analyse:

A) Would this particular execution have been 'salvaged' if more gas had been provided by the external caller?
B) If not, would the `POKE` precompile have 'salvaged' it?
C) If not, would the tx-access list have 'salvaged' it?

For 2), it is interesting to analyse:

A) What was the difference in gas used by the transaction? Did the `alternative` transaction consume more or less?


### Goerli results. 


There were `100` transactions that were `OK`, as in, the execution finished the same way in both the 'canon' version
and the 'alt' (gas-cost-increase version):

| txhash | steps(canon) | steps(alt) | OK? |  gas(canon) |  gas(alt) | diff | 
| ------ | ------------ | ---------- | --- | -----------| ---------| -----| 
 0x26888356 | 15570 | 15570 | ok | 469226 | 512826 | 9.00 %|
 0x9f795798 | 1 | 1 | ok | 0 | 0 | 0.00 %|
 0xf89eb38e | 340 | 340 | ok | 31967 | 34067 | 6.00 %|
 0xa0084529 | 15630 | 15630 | ok | 412982 | 418582 | 1.00 %|
 0xcf9553b2 | 15630 | 15630 | ok | 412982 | 418582 | 1.00 %|
 0x5768df5e | 1 | 1 | ok | 0 | 0 | 0.00 %|
 0xb33b6d6d | 1 | 1 | ok | 0 | 0 | 0.00 %|
 0xb6dce779 | 15630 | 15630 | ok | 412982 | 418582 | 1.00 %|
 0x20313f8f | 1411 | 1411 | ok | 76144 | 87844 | 15.00 %|
 0xbf98737d | 1 | 1 | ok | 0 | 0 | 0.00 %|
 0x04b95f1b | 258 | 258 | ok | 29362 | 29762 | 1.00 %|
 0x5867d811 | 15630 | 15630 | ok | 412982 | 418582 | 1.00 %|
 0x6e4496c7 | 15630 | 15630 | ok | 412982 | 418582 | 1.00 %|
 0x7e005bb0 | 1 | 1 | ok | 0 | 0 | 0.00 %|
 0x84a35acb | 15630 | 15630 | ok | 412982 | 418582 | 1.00 %|
 0xe10171a6 | 1 | 1 | ok | 0 | 0 | 0.00 %|
 0x3fd24de9 | 377 | 377 | ok | 15488 | 15088 | -3.00 %|
 0x3cca6923 | 377 | 377 | ok | 15488 | 15088 | -3.00 %|
 0xd787848a | 377 | 377 | ok | 15488 | 15088 | -3.00 %|
 0xb70224df | 15630 | 15630 | ok | 412982 | 418582 | 1.00 %|
 0x8f60fe0d | 377 | 377 | ok | 15488 | 15088 | -3.00 %|
 0xcd7e7ce6 | 15630 | 15630 | ok | 412982 | 418582 | 1.00 %|
 0x5891f568 | 6325 | 6325 | ok | 298960 | 306360 | 2.00 %|
 0x578a51ef | 23990 | 23990 | ok | 906184 | 940984 | 3.00 %|
 0x848ebe81 | 258 | 258 | ok | 29362 | 29762 | 1.00 %|
 0x9fdf8667 | 377 | 377 | ok | 15488 | 15088 | -3.00 %|
 0xef2b2bf2 | 258 | 258 | ok | 29362 | 29762 | 1.00 %|
 0x6770fd04 | 1 | 1 | ok | 0 | 0 | 0.00 %|
 0xf276ac64 | 6325 | 6325 | ok | 298960 | 306360 | 2.00 %|
 0x94826b3d | 1 | 1 | ok | 0 | 0 | 0.00 %|
 0xf7c56b8f | 15630 | 15630 | ok | 432182 | 438482 | 1.00 %|
 0x8973962a | 6332 | 6332 | ok | 298980 | 302080 | 1.00 %|
 0x171ab5c7 | 6257 | 6257 | ok | 169712 | 153712 | -10.00 %|
 0x9577d126 | 258 | 258 | ok | 29362 | 29762 | 1.00 %|
 0x9301dd6d | 6325 | 6325 | ok | 298960 | 306360 | 2.00 %|
 0x2c10f55a | 258 | 258 | ok | 29362 | 29762 | 1.00 %|
 0x44392316 | 1 | 1 | ok | 0 | 0 | 0.00 %|
 0x75daeceb | 258 | 258 | ok | 29362 | 27862 | -6.00 %|
 0x0222d6cf | 15630 | 15630 | ok | 432182 | 438482 | 1.00 %|
 0x44df7cfa | 377 | 377 | ok | 15488 | 9388 | -40.00 %|
 0xbdc1c6cf | 6325 | 6325 | ok | 298960 | 306360 | 2.00 %|
 0x23029eec | 6325 | 6325 | ok | 298960 | 267360 | -11.00 %|
 0x2c207531 | 15630 | 15630 | ok | 412982 | 418582 | 1.00 %|
 0x1a8d48e5 | 6325 | 6325 | ok | 298960 | 306360 | 2.00 %|
 0x37f83d52 | 258 | 258 | ok | 29362 | 27862 | -6.00 %|
 0x5395285e | 1 | 1 | ok | 0 | 0 | 0.00 %|
 0xadfacf22 | 502 | 502 | ok | 19854 | 24254 | 22.00 %|
 0x9331a030 | 1 | 1 | ok | 0 | 0 | 0.00 %|
 0x5b7ea6ac | 377 | 377 | ok | 15488 | 15088 | -3.00 %|
 0xce51e39e | 15630 | 15630 | ok | 412982 | 418582 | 1.00 %|
 0x27147082 | 377 | 377 | ok | 15488 | 15088 | -3.00 %|
 0x9e4b02ee | 258 | 258 | ok | 29362 | 29762 | 1.00 %|
 0x561ca5d8 | 6332 | 6332 | ok | 298980 | 306380 | 2.00 %|
 0x9ea5e140 | 6332 | 6332 | ok | 298980 | 267380 | -11.00 %|
 0xdbead36b | 377 | 377 | ok | 15488 | 15088 | -3.00 %|
 0x8c33128d | 258 | 258 | ok | 29362 | 29762 | 1.00 %|
 0x0150ed20 | 340 | 340 | ok | 12767 | 12267 | -4.00 %|
 0x0f9a5a0f | 377 | 377 | ok | 15488 | 15088 | -3.00 %|
 0x26eecdb0 | 258 | 258 | ok | 29362 | 29762 | 1.00 %|
 0xd96c736a | 6044 | 6044 | ok | 124673 | 96873 | -23.00 %|
 0x68622456 | 6325 | 6325 | ok | 298960 | 267360 | -11.00 %|
 0x7a180660 | 1 | 1 | ok | 0 | 0 | 0.00 %|
 0xd356e16c | 15630 | 15630 | ok | 432182 | 438482 | 1.00 %|
 0xcbd02f65 | 6044 | 6044 | ok | 124673 | 101073 | -19.00 %|
 0xda048c47 | 377 | 377 | ok | 15488 | 15088 | -3.00 %|
 0xdf322b2a | 1 | 1 | ok | 0 | 0 | 0.00 %|
 0xa66cdfe8 | 1 | 1 | ok | 0 | 0 | 0.00 %|
 0x550770b3 | 15731 | 15731 | ok | 1149087 | 1201887 | 4.00 %|
 0xcf57527b | 6257 | 6257 | ok | 169712 | 153712 | -10.00 %|
 0x113897c1 | 377 | 377 | ok | 15488 | 15088 | -3.00 %|
 0xb07f73f6 | 258 | 258 | ok | 29362 | 27862 | -6.00 %|
 0xe1883f43 | 1 | 1 | ok | 0 | 0 | 0.00 %|
 0xf07e2c52 | 210 | 210 | ok | 1518087 | 1518087 | 0.00 %|
 0x55c2d6df | 377 | 377 | ok | 15488 | 15088 | -3.00 %|
 0x7499547c | 15570 | 15570 | ok | 469226 | 512826 | 9.00 %|
 0xb917dc67 | 1 | 1 | ok | 0 | 0 | 0.00 %|
 0x420cd0e2 | 6332 | 6332 | ok | 298980 | 302080 | 1.00 %|
 0x90b1ec09 | 377 | 377 | ok | 15488 | 15088 | -3.00 %|
 0xd5d7cf5c | 6257 | 6257 | ok | 169712 | 149512 | -12.00 %|
 0xfadc30ea | 15630 | 15630 | ok | 412982 | 418582 | 1.00 %|
 0x0dffecb4 | 6325 | 6325 | ok | 298960 | 306360 | 2.00 %|
 0xf7151f6f | 258 | 258 | ok | 29362 | 29762 | 1.00 %|
 0x5c72a21a | 15630 | 15630 | ok | 412982 | 418582 | 1.00 %|
 0x1d29f0b2 | 377 | 377 | ok | 15488 | 15088 | -3.00 %|
 0xcdd7a3d5 | 377 | 377 | ok | 15488 | 15088 | -3.00 %|
 0x672f1027 | 1 | 1 | ok | 0 | 0 | 0.00 %|
 0x2f4c2c25 | 258 | 258 | ok | 29362 | 27862 | -6.00 %|
 0x60f5268a | 1 | 1 | ok | 0 | 0 | 0.00 %|
 0xac1c6cfe | 377 | 377 | ok | 15488 | 15088 | -3.00 %|
 0xd41659a7 | 1 | 1 | ok | 0 | 0 | 0.00 %|
 0x71435959 | 1 | 1 | ok | 0 | 0 | 0.00 %|
 0x10e72aa7 | 6257 | 6257 | ok | 169712 | 149512 | -12.00 %|
 0xfd89999c | 6243 | 6243 | ok | 169658 | 153658 | -10.00 %|
 0xd690c177 | 15630 | 15630 | ok | 412982 | 418582 | 1.00 %|
 0xadef95d2 | 1 | 1 | ok | 0 | 0 | 0.00 %|
 0x9e1662e4 | 377 | 377 | ok | 15488 | 15088 | -3.00 %|
 0xa97ab7a7 | 1 | 1 | ok | 0 | 0 | 0.00 %|
 0x643d441f | 1 | 1 | ok | 0 | 0 | 0.00 %|
 0x50f7d372 | 6332 | 6332 | ok | 298980 | 306380 | 2.00 %|
 0xff5bbcff | 15731 | 15731 | ok | 1149087 | 1201887 | 4.00 %|


And `6` transactions were 'broken':

| txhash | steps(canon) | steps(alt) | OK? |  gas(canon) |  gas(alt) | diff | 
| ------ | ------------ | ---------- | --- | -----------| ---------| -----| 
 0xd67b5067 | 557 | 547 | BROKEN | 46354 | 46354 | 0.00 %|
 0x8574e95d | 3297 | 3187 | BROKEN | 519530 | 519530 | 0.00 %|
 0xfc2b04ed | 4775 | 2640 | BROKEN | 199854 | 193405 | -4.00 %|
 0xe85c0e23 | 369 | 362 | BROKEN | 61215 | 61215 | 0.00 %|
 0xaeb93809 | 15119 | 12479 | BROKEN | 400331 | 382875 | -5.00 %|
 0xef39d3b1 | 64117 | 61780 | BROKEN | 4398883 | 4400712 | 0.00 %|


### Broken flows

Let's look deeper into the broken ones: 

#### `0xd67b5067` 

`block_0x19ef4a84-2-0xd67b5067-742912372`:
```

─────────────────────────Operations─────────────────────────┐┌─────────────────────────Operations──────────────────────────┐
│STEP      PC       OPNAME  OPCODE GAS  GASCOST DEPTH REFUND ││STEP      PC      OPNAME OPCODE GAS  GASCOST DEPTH REFUND    │
│538  2724 (0xaa4) POP      0x50   8187 2       1     0      ││528  2714 (0xa9a) ADD    0x1    5714 3       1     0         │
│539  2725 (0xaa5) POP      0x50   8185 2       1     0      ││529  2715 (0xa9b) DUP3   0x82   5711 3       1     0         │
│540  2726 (0xaa6) POP      0x50   8183 2       1     0      ││530  2716 (0xa9c) SWAP1  0x90   5708 3       1     0         │
│541  2727 (0xaa7) POP      0x50   8181 2       1     0      ││531  2717 (0xa9d) SUB    0x3    5705 3       1     0         │
│542  2728 (0xaa8) POP      0x50   8179 2       1     0      ││532  2718 (0xa9e) SWAP11 0x9a   5702 3       1     0         │
│543  2729 (0xaa9) POP      0x50   8177 2       1     0      ││533  2719 (0xa9f) POP    0x50   5699 2       1     0         │
│544  2730 (0xaaa) POP      0x50   8175 2       1     0      ││534  2720 (0xaa0) SWAP1  0x90   5697 3       1     0         │
│545  2731 (0xaab) LOG1     0xa1   8173 8150    1     0      ││535  2721 (0xaa1) SWAP9  0x98   5694 3       1     0         │
│546  2732 (0xaac) POP      0x50   23   2       1     0      ││536  2722 (0xaa2) POP    0x50   5691 2       1     0         │
│547  2733 (0xaad) POP      0x50   21   2       1     0      ││537  2723 (0xaa3) POP    0x50   5689 2       1     0         │
│548  2734 (0xaae) POP      0x50   19   2       1     0      ││538  2724 (0xaa4) POP    0x50   5687 2       1     0         │
│549  2735 (0xaaf) POP      0x50   17   2       1     0      ││539  2725 (0xaa5) POP    0x50   5685 2       1     0         │
│550  2736 (0xab0) POP      0x50   15   2       1     0      ││540  2726 (0xaa6) POP    0x50   5683 2       1     0         │
│551  2737 (0xab1) POP      0x50   13   2       1     0      ││541  2727 (0xaa7) POP    0x50   5681 2       1     0         │
│552  2738 (0xab2) POP      0x50   11   2       1     0      ││542  2728 (0xaa8) POP    0x50   5679 2       1     0         │
│553  2739 (0xab3) JUMP     0x56   9    8       1     0      ││543  2729 (0xaa9) POP    0x50   5677 2       1     0         │
│554  426 (0x1aa)  JUMPDEST 0x5b   1    1       1     0      ││544  2730 (0xaaa) POP    0x50   5675 2       1     0         │
│555  427 (0x1ab)  STOP     0x0    0    0       1     0      ││545  2731 (0xaab) LOG1   0xa1   5673 8150    1     0         │
└────────────────────────────────────────────────────────────┘└─────────────────────────────────────────────────────────────┘

```
This tx breaks on a `LOG1` instruction on the outermost `depth`. Therefore, it would have succeeded with some more gas from the `EOA`. 
It can also be noted that the `canon` tx also went `OOG`, so technically there was no change. 

#### `0x8574e95d`

This tx also goes OOG in the uppermost `depth`, at step `3185`, where it hits an `SSTORE`. The `canon` tx has `63K` gas left at this 
point, but the `alt` has only `11K`. This is also a situation where more gas from outside would have salvaged the call. 

It can also be noted that for this transaction too, the `canon` tx also went `OOG`, so technically there was no change. 

#### `0xfc2b04ed`

This tx is actually different - the canon tx does _not_ go `OOG`. The `canon` transaction does a series of 
deep calls, and goes through `4773` steps of execution. 
The 'alt' transaction fails at step `2638`. However, the execution differs even earlier :
```
┌─────────────────────────Operations─────────────────────────┐┌─────────────────────────Operations──────────────────────────┐
│STEP       PC        OPNAME  OPCODE  GAS  GASCOST DEPTH EFU…││STEP       PC           OPNAME     OPCODE GAS  GASCOST DEPTH │
│2591 18041 (0x4679) SWAP2    0x91   43718 3       4     0   ││2591 18041 (0x4679) SWAP2          0x91   4571 3       4     │
│2592 18042 (0x467a) SSTORE   0x55   43715 800     4     0   ││2592 18042 (0x467a) SSTORE         0x55   4568 2100    4     │
│2593 18043 (0x467b) PUSH1    0x60   42915 3       4     0   ││2593 18043 (0x467b) PUSH1          0x60   2468 3       4     │
│2594 18045 (0x467d) SSTORE   0x55   42912 5000    4     0   ││2594 18045 (0x467d) SSTORE         0x55   2465 3000    4     │
│2595 18046 (0x467e) JUMP     0x56   37912 8       4     0   ││2595 607 (0x25f)    RETURNDATASIZE 0x3d   8097 2       3     │
│2596 4899 (0x1323)  JUMPDEST 0x5b   37904 1       4     0   ││2596 608 (0x260)    PUSH1          0x60   8095 3       3     │
│2597 4900 (0x1324)  PUSH2    0x61   37903 3       4     0   ││2597 610 (0x262)    MLOAD          0x51   8092 3       3     │
│2598 4903 (0x1327)  DUP2     0x81   37900 3       4     0   ││2598 611 (0x263)    DUP2           0x81   8089 3       3     │
```
At step `2594`, a call at depth `4` exits with `OOG`. The call was initiated at step `1229`, and is a `DELEGATECALL` with `gas` not being hardcoded, but `GAS`.  


Call ladder:

1. delegatecall(GAS)
2. call(GAS)
3. delegatecall(GAS)

Since the `gas` is never restricted, it appears that this tx would have been salvageable with more outer gas. 

#### `0x8574e95d`


The `0x8574e95d` transaction has `3295` canon steps, but exits early after `3185` steps on 'alt', where an `SSTORE` occurs, causing `OOG`. 
The event happens on `depth=1`, meaning that more outer gas would have salvaged the flow. 

#### `0xfc2b04ed`

The `0xfc2b04ed` tx has `4773` steps, but the 'alt' is aborted after '2638' steps. 
However, the execution flow is disrupted at step `2594`, where an `SSTORE` at `depth=4` causes a
subcall to go `OOG`:
```
─────────────────────────Operations─────────────────────────┐┌─────────────────────────Operations──────────────────────────┐
│STEP       PC        OPNAME  OPCODE  GAS  GASCOST DEPTH EFU…││STEP       PC           OPNAME     OPCODE GAS  GASCOST DEPTH │
│2591 18041 (0x4679) SWAP2    0x91   43718 3       4     0   ││2591 18041 (0x4679) SWAP2          0x91   4571 3       4     │
│2592 18042 (0x467a) SSTORE   0x55   43715 800     4     0   ││2592 18042 (0x467a) SSTORE         0x55   4568 2100    4     │
│2593 18043 (0x467b) PUSH1    0x60   42915 3       4     0   ││2593 18043 (0x467b) PUSH1          0x60   2468 3       4     │
│2594 18045 (0x467d) SSTORE   0x55   42912 5000    4     0   ││2594 18045 (0x467d) SSTORE         0x55   2465 3000    4     │
│2595 18046 (0x467e) JUMP     0x56   37912 8       4     0   ││2595 607 (0x25f)    RETURNDATASIZE 0x3d   8097 2       3     │
│2596 4899 (0x1323)  JUMPDEST 0x5b   37904 1       4     0   ││2596 608 (0x260)    PUSH1          0x60   8095 3       3     │
│2597 4900 (0x1324)  PUSH2    0x61   37903 3       4     0   ││2597 610 (0x262)    MLOAD          0x51   8092 3       3     │
│2598 4903 (0x1327)  DUP2     0x81   37900 3       4     0   ││2598 611 (0x263)    DUP2           0x81   8089 3       3     │
│2599 4904 (0x1328)  DUP6     0x85   37897 3       4     0   ││2599 612 (0x264)    PUSH1          0x60   8086 3       3     │
│2600 4905 (0x1329)  DUP12    0x8b   37894 3       4     0   ││2600 614 (0x266)    DUP3           0x82   8083 3       3     │
│2601 4906 (0x132a)  DUP10    0x89   37891 3       4     0   ││2601 615 (0x267)    RETURNDATACOPY 0x3e   8080 3       3     │
└────────────────────────────────────────────────────────────┘└─────────────────────────────────────────────────────────────┘
```

Call ladder:

1.  DCALL(GAS-10000) to 0x6b8a780124a2259b... (ctx: NA)                   
2.  CALL(GAS) to 0x5b67626cbf5d1677...                              
3.  DCALL(GAS) to 0xfe488f251a7c6e63... (ctx: 0x5b67626cbf5d1677...)

It seems that this one would have been salvaged by more external gas. 

### `0xe85c0e23`

The `0xe85c0e23` goes `OOG` at step `360`, where it does a `LOG2` operation, where the 'canon' trace continues another `7` steps. 
This happens at `depth=1`, meaning that more external gas would have solved it. 

### `0xaeb93809`

This is a very long trace, reaching depths of `6`. 
The execution flow is diverted at depth `6`, on step `12405`, where an `SSTORE` causes `OOG`:

```
┌─────────────────────────Operations─────────────────────────┐┌─────────────────────────Operations──────────────────────────┐
│STEP        PC        OPNAME  OPCODE  GAS  GASCOST DEPTH EF…││STEP        PC           OPNAME     OPCODE GAS  GASCOST DEPTH│
│12398 9075 (0x2373)  POP      0x50   50012 2       6     0  ││12398 9075 (0x2373)  POP            0x50   1275 2       6    │
│12399 9076 (0x2374)  POP      0x50   50010 2       6     0  ││12399 9076 (0x2374)  POP            0x50   1273 2       6    │
│12400 9077 (0x2375)  JUMP     0x56   50008 8       6     0  ││12400 9077 (0x2375)  JUMP           0x56   1271 8       6    │
│12401 10784 (0x2a20) JUMPDEST 0x5b   50000 1       6     0  ││12401 10784 (0x2a20) JUMPDEST       0x5b   1263 1       6    │
│12402 10785 (0x2a21) PUSH1    0x60   49999 3       6     0  ││12402 10785 (0x2a21) PUSH1          0x60   1262 3       6    │
│12403 10787 (0x2a23) DUP2     0x81   49996 3       6     0  ││12403 10787 (0x2a23) DUP2           0x81   1259 3       6    │
│12404 10788 (0x2a24) SWAP1    0x90   49993 3       6     0  ││12404 10788 (0x2a24) SWAP1          0x90   1256 3       6    │
│12405 10789 (0x2a25) SSTORE   0x55   49990 5000    6     0  ││12405 10789 (0x2a25) SSTORE         0x55   1253 0       6    │
│12406 10790 (0x2a26) POP      0x50   44990 2       6     0  ││12406 684 (0x2ac)    RETURNDATASIZE 0x3d   9897 2       5    │
│12407 10791 (0x2a27) PUSH1    0x60   44988 3       6     0  ││12407 685 (0x2ad)    PUSH1          0x60   9895 3       5    │
│12408 10793 (0x2a29) PUSH2    0x61   44985 3       6     0  ││12408 687 (0x2af)    MLOAD          0x51   9892 3       5    │
│12409 10796 (0x2a2c) DUP3     0x82   44982 3       6     0  ││12409 688 (0x2b0)    DUP2           0x81   9889 3       5    │
│12410 10797 (0x2a2d) DUP7     0x86   44979 3       6     0  ││12410 689 (0x2b1)    PUSH1          0x60   9886 3       5    │
│12411 10798 (0x2a2e) PUSH2    0x61   44976 3       6     0  ││12411 691 (0x2b3)    DUP3           0x82   9883 3       5    │
│12412 10801 (0x2a31) SWAP1    0x90   44973 3       6     0  ││12412 692 (0x2b4)    RETURNDATACOPY 0x3e   9880 3       5    │
│12413 10802 (0x2a32) SWAP2    0x91   44970 3       6     0  ││12413 693 (0x2b5)    DUP3           0x82   9877 3       5    │
└────────────────────────────────────────────────────────────┘└─────────────────────────────────────────────────────────────┘
```

Call ladder: 

```
call 4  DCALL to 0xfd259808f4c08b12... 
	- gas = `GAS-10K`
call 3  CALL to 0xf5e574045298ee3a... 
	- gas = `GAS`
call 2  DCALL to 0x25723f81ebf997f3... 
	- gas = `GAS-10K`
call 1  CALL to 0x00200ea4ee292e25... 
	- gas = `GAS`
call 0  DCALL to 0xce29aedcdbeef0b0... 
	- gas = `GAS-10K`
```

Since this uses `GAS` (minus some constant), it seems likely that this could also be salvaged by using more external gas. 

### `0xef39d3b1`

This is another extremely long trace, with `60K+` steps. At step `61764`, at depth `2`, an `SLOAD` causes the 'alt'-trace to go OOG. 
The depth `2` was reached via a `DELEGATECALL(GAS...)`, so it appears that this would also have been salvageable via more external gas. 

## Summary

The test on `Goerli`, covering `106` transactions, showed

- Out of `106` transactions, `100` were not meaningfully affected by the change, 
- For those `100` transactions, 
	- The 'canon' gas used was `18111863`, 
	- and the 'alt' gas used was `18264363`, which is `+0.84%`.
- Out of the `6` failing transactions, 
	- `2` went `OOG` in the 'canon' version aswell as in the `alt` version
	- All `6` seems to have been salvageable by using more external gas by the caller. 
