/* 
 * CS:APP Data Lab 
 * 
 * Christopher Jarek,
 * 101854209
 * 
 * bits.c - Source file with your solutions to the Lab.
 *          This is the file you will hand in to your instructor.
 *
 * WARNING: Do not include the <stdio.h> header; it confuses the dlc
 * compiler. You can still use printf for debugging without including
 * <stdio.h>, although you might get a compiler warning. In general,
 * it's not good practice to ignore compiler warnings, but in this
 * case it's OK.  
 */

#if 0
/*
 * Instructions to Students:
 *
 * STEP 1: Read the following instructions carefully.
 */

You will provide your solution to the Data Lab by
editing the collection of functions in this source file.

INTEGER CODING RULES:
 
  Replace the "return" statement in each function with one
  or more lines of C code that implements the function. Your code 
  must conform to the following style:
 
  int Funct(arg1, arg2, ...) {
      /* brief description of how your implementation works */
      int var1 = Expr1;
      ...
      int varM = ExprM;

      varJ = ExprJ;
      ...
      varN = ExprN;
      return ExprR;
  }

  Each "Expr" is an expression using ONLY the following:
  1. Integer constants 0 through 255 (0xFF), inclusive. You are
      not allowed to use big constants such as 0xffffffff.
  2. Function arguments and local variables (no global variables).
  3. Unary integer operations ! ~
  4. Binary integer operations & ^ | + << >>
    
  Some of the problems restrict the set of allowed operators even further.
  Each "Expr" may consist of multiple operators. You are not restricted to
  one operator per line.

  You are expressly forbidden to:
  1. Use any control constructs such as if, do, while, for, switch, etc.
  2. Define or use any macros.
  3. Define any additional functions in this file.
  4. Call any functions.
  5. Use any other operations, such as &&, ||, -, or ?:
  6. Use any form of casting.
  7. Use any data type other than int.  This implies that you
     cannot use arrays, structs, or unions.

 
  You may assume that your machine:
  1. Uses 2s complement, 32-bit representations of integers.
  2. Performs right shifts arithmetically.
  3. Has unpredictable behavior when shifting an integer by more
     than the word size.

EXAMPLES OF ACCEPTABLE CODING STYLE:
  /*
   * pow2plus1 - returns 2^x + 1, where 0 <= x <= 31
   */
  int pow2plus1(int x) {
     /* exploit ability of shifts to compute powers of 2 */
     return (1 << x) + 1;
  }

  /*
   * pow2plus4 - returns 2^x + 4, where 0 <= x <= 31
   */
  int pow2plus4(int x) {
     /* exploit ability of shifts to compute powers of 2 */
     int result = (1 << x);
     result += 4;
     return result;
  }

FLOATING POINT CODING RULES

For the problems that require you to implent floating-point operations,
the coding rules are less strict.  You are allowed to use looping and
conditional control.  You are allowed to use both ints and unsigneds.
You can use arbitrary integer and unsigned constants.

You are expressly forbidden to:
  1. Define or use any macros.
  2. Define any additional functions in this file.
  3. Call any functions.
  4. Use any form of casting.
  5. Use any data type other than int or unsigned.  This means that you
     cannot use arrays, structs, or unions.
  6. Use any floating point data types, operations, or constants.


NOTES:
  1. Use the dlc (data lab checker) compiler (described in the handout) to 
     check the legality of your solutions.
  2. Each function has a maximum number of operators (! ~ & ^ | + << >>)
     that you are allowed to use for your implementation of the function. 
     The max operator count is checked by dlc. Note that '=' is not 
     counted; you may use as many of these as you want without penalty.
  3. Use the btest test harness to check your functions for correctness.
  4. Use the BDD checker to formally verify your functions
  5. The maximum number of ops for each function is given in the
     header comment for each function. If there are any inconsistencies 
     between the maximum ops in the writeup and in this file, consider
     this file the authoritative source.

/*
 * STEP 2: Modify the following functions according the coding rules.
 * 
 *   IMPORTANT. TO AVOID GRADING SURPRISES:
 *   1. Use the dlc compiler to check that your solutions conform
 *      to the coding rules.
 *   2. Use the BDD checker to formally verify that your solutions produce 
 *      the correct answers.
 */


#endif
/* Copyright (C) 1991-2016 Free Software Foundation, Inc.
   This file is part of the GNU C Library.

   The GNU C Library is free software; you can redistribute it and/or
   modify it under the terms of the GNU Lesser General Public
   License as published by the Free Software Foundation; either
   version 2.1 of the License, or (at your option) any later version.

   The GNU C Library is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   Lesser General Public License for more details.

   You should have received a copy of the GNU Lesser General Public
   License along with the GNU C Library; if not, see
   <http://www.gnu.org/licenses/>.  */
/* This header is separate from features.h so that the compiler can
   include it implicitly at the start of every compilation.  It must
   not itself include <features.h> or any other header that includes
   <features.h> because the implicit include comes before any feature
   test macros that may be defined in a source file before it first
   explicitly includes a system header.  GCC knows the name of this
   header in order to preinclude it.  */
/* glibc's intent is to support the IEC 559 math functionality, real
   and complex.  If the GCC (4.9 and later) predefined macros
   specifying compiler intent are available, use them to determine
   whether the overall intent is to support these features; otherwise,
   presume an older compiler has intent to support these features and
   define these macros by default.  */
/* wchar_t uses Unicode 8.0.0.  Version 8.0 of the Unicode Standard is
   synchronized with ISO/IEC 10646:2014, plus Amendment 1 (published
   2015-05-15).  */
/* We do not support C11 <threads.h>.  */



/* 
 * allEvenBits - return 1 if all even-numbered bits in word set to 1
 *   Examples allEvenBits(0xFFFFFFFE) = 0, allEvenBits(0x55555555) = 1
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 12
 *   Rating: 2
 */
// Problem 1
int allEvenBits(int x) {
  //I used the same method as in bitParity to "compress" each bit down to the least significant 2 bits
  //once compressed in this way it's compared to "01"
  //x = 1 0 1 0 1 0 1 0
  //x = (x >> 4) & x; => (1) (0) (1) (0) (1&1) (0&0) (1&1) (0&0)
  //x = (x >> 2) & x; => (1) (0) (1&1) (0&0) (1&1&1) (0&0&0) (1&1&1&1) (0&0&0&0)
  //above is a simplified example of how this algorithm works, it essentially stacks each bit into the first 2
  //using & operators it can keep track of if each even bit is 1.

  x = (x >> 16) & x;
  x = (x >> 8) & x;
  x = (x >> 4) & x;
  x = (x >> 2) & x;

  return x & 0x01;
}
/*
 * bitParity - returns 1 if x contains an odd number of 0's
 *   Examples: bitParity(5) = 0, bitParity(7) = 1
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 20
 *   Rating: 4
 */
// Problem 2
int bitParity(int x) {
  //This problem was quite confusing but by using XOR between x and x shifted by some factor of 2
  //we can "gather" each XOR'd bit into the least significant bit, which results in a 1 if there is an
  //odd number of 1's in the int. We then have to use ! to flip our solution to align with the intended output
  //
  //This solution can be demonstrated by working through the shifts one by one (for a 4 bit int we skip to x >> 2)
  //x = 1 2 3 4
  //x ^ (x >> 2) => (1)(2)(1^3)(2^4)
  //x ^ (x >> 1) => (1)(1^2)(1^2^3)(1^2^3^4)
  //we can then & our final x with 0001 to get a single bit representation of the int's parity

  x = x ^ (x >> 16);
  x = x ^ (x >> 8);
  x = x ^ (x >> 4);
  x = x ^ (x >> 2);
  x = x ^ (x >> 1);

  


  return x & 0x01;
}
/* 
 * bitXor - x^y using only ~ and & 
 *   Example: bitXor(4, 5) = 1
 *   Legal ops: ~ &
 *   Max ops: 14
 *   Rating: 1
 */
// Problem 3
int bitXor(int x, int y) {
  //using ~(a&b) we can create NAND which gives us the following logic table
  //[1 1 0 0] NAND [1 0 1 0] => [0 1 1 1]
  //we then create x and y components by using NAND on x and y with xNANDy individually
  //[1 1 0 0] NAND [0 1 1 1] => [1 0 1 1]
  //[1 0 1 0] NAND [0 1 1 1] => [1 1 0 1]
  //finally using NAND between these two components gives:
  //[1 0 1 1] NAND [1 1 0 1] => [0 1 1 0]
  //which is equivilant to XOR:
  //[1 1 0 0] XOR [1 0 1 0] => [0 1 1 0]

  int xNANDy = ~(x & y);
  int xComponent = ~(x & xNANDy);
  int yComponent = ~(y & xNANDy);
  int output = ~(xComponent & yComponent);

  return output;
}
/* 
 * leastBitPos - return a mask that marks the position of the
 *               least significant 1 bit. If x == 0, return 0
 *   Example: leastBitPos(96) = 0x20
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 6
 *   Rating: 2 
 */
// Problem 4
int leastBitPos(int x) {
  //The final result is a combination of the below steps in order to simplify the code.
  //unsigned int notX = ~x;
  //unsigned int notXplusOne = notX + 1;
  //unsigned int mask = x & notXplusOne;
  //By adding one to the inverse of x we can mark the least positive bit with a 1
  //this is because any bit smaller than the least positive becomes 1 when inverted
  //and when 1 is added they all flip again to 0, leaving the least positive bit as 1 since it was 0
  //we can then & this with the original input to remove any other extra 1's created by the inversion.

  
  return x & (~x + 1);
}
/* 
 * replaceByte(x,n,c) - Replace byte n in x with c
 *   Bytes numbered from 0 (LSB) to 3 (MSB)
 *   Examples: replaceByte(0x12345678,1,0xab) = 0x1234ab78
 *   You can assume 0 <= n <= 3 and 0 <= c <= 255
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 10
 *   Rating: 3
 */
// Problem 5
int replaceByte(int x, int n, int c) {
  //given an input of 0x12345678
  //we can read it as 12 34 56 78 with the rightmost pair being position 0
  //increasing to 3 in the leftmost position.
  //Each of these bytes corresponds to 8 bits thus we can remove the selected region by rightsifting 8*n times
  //this shift can be rewritten as (n << 3) as leftshifting 3 times is equivilant to multiplying by 8
  //We can then replace the lost bytes by leftshifting 8 times and adding c
  //This however causes us to lose the remaining bytes to the right of the selected region so we can 'save' them using a temp variable
  
  int mask = (0xff << (n << 3));
  int newC = c << (n << 3);
  return (x & ~mask) | newC;
}
/* 
 * TMax - return maximum two's complement integer 
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 4
 *   Rating: 1
 */
// Problem 6
int tmax(void) {
  //the maximum 2's complement int, assuming a 32 bit system is 31 1's in binary, since the 32'nd bit is reserved for the sign
  //this can be represented by left shifting a 1, 32 times then subtracting 1, flipping the 32'nd bit to 0 and the rest to 1's
   int output = (1 << 31) ^ (~0);
  return output;
}
/* 
 * fitsBits - return 1 if x can be represented as an 
 *  n-bit, two's complement integer.
 *   1 <= n <= 32
 *   Examples: fitsBits(5,3) = 0, fitsBits(-4,3) = 1
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 15
 *   Rating: 2
 */
// Problem 7
int fitsBits(int x, int n) {
  //we need to find a way to return 1 if x can fit within n-1 bits, this is because a size n 2's complement integer reserves its
  //leftmost bit to display sign, therefore a 2 bit 2's complement integer can only display -1, 0, 1.
  //we can do this by "clearing" the leftmost (n + 1) bits by leftshifting then rightshifting by that amount
  //if the number can be represented within the allowed number of bits then it will remain equal to the shifted number
  //if it cannot be represented with the given number of bits, then it will have lost some of its most significant bitss
  //therefore if we use XOR between our original number, and our shifted number, we can get an answer of Ox00... if the number
  //can be represented within the allowed bits or we get some nonzero number if it cannot. Either way we can then use ! to
  //get our final answer which is consistant with the prompt.

  int shiftedRight = x >> (n + (~0));
  int mask = x >> 31;
  return !(shiftedRight ^ mask);
}
/* 
 * divpwr2 - Compute x/(2^n), for 0 <= n <= 30
 *  Round toward zero
 *   Examples: divpwr2(15,1) = 7, divpwr2(-33,4) = -2
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 15
 *   Rating: 2
 */
// Problem 8
int divpwr2(int x, int n) {
  //dividing by 2 using binary operators is simple enough, just right-shift x by n to get x/2^n
  //since any remainder digits are lost through the right shift, the result is automatically rounded down
  //we also need to consider the sign bit, which we can save by rightshifting x 31 times
  int signMask = (x >> 31);
  int posTest = ((1 << n) + (~0)) & x;

  return (x >> n) + (signMask & (!!posTest));
}
/* 
 * isEqual - return 1 if x == y, and 0 otherwise 
 *   Examples: isEqual(5,5) = 1, isEqual(4,5) = 0
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 5
 *   Rating: 2
 */
// Problem 9
int isEqual(int x, int y) {
  //to check if x and y are equal we can use the xor operator, ^
  //the resulting int will be Ox00 if x and y are equal. We can then use the not operator, !
  //to convert Ox00 into 1 and anything else into 0

  return !(x ^ y);

}
/* 
 * isPositive - return 1 if x > 0, return 0 otherwise 
 *   Example: isPositive(-1) = 0.
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 8
 *   Rating: 3
 */
// Problem 10
int isPositive(int x) {
  //this solution is easy to determine once we realize that c uses two's compliment to represent positive and negative ints
  //from this we can simply reference our knowledge of two's compliment representation to know that the most significant bit
  //is used to indicate sign. 1 means positive, 0 means negative. Because of this all we have to do is disregard the other 31 bits
  //and flip the 32nd bit to get our output.

  //for the case that x = 0, the accepted solution is 0. This means that we must account for this by using & with !!x.

  return !(x >> 31) & (!!x);
}
/* 
 * subOK - Determine if can compute x-y without overflow
 *   Example: subOK(0x80000000,0x80000000) = 1,
 *            subOK(0x80000000,0x70000000) = 0, 
 *   Legal ops: ! ~ & ^ | + << >>
 *   Max ops: 20
 *   Rating: 3
 */
// Problem 11
int subOK(int x, int y) {
  //an overflow happens for two different reasons, if x and y have the same sign, and if y > x is true.
  //we can use & to compare the results of our two evaluations to determine if both conditions are true.
  //below is a simple evaluation of hasSameSign, however determining if y > x without actually doing the computation
  //is much more difficult.
  //Since ints are represented in 2's complement, we can determine if y > x by converting y into -y using 2's complement
  //then preforming an addition (this is sorta like subtraction but done in a way that avoids any overflow)
  //we can then check the most significant sign of the resulting number. It will be a 1 if x is less than y and 0 otherwise

  //my initial method fails when attempting to subtract either x - 0 or x - x. To fix this I decided to actually peprform
  //the subtraction by converting y into its negative 2's compliment and adding it to x.
  //by using this instead of the greaterThanOrEqual check I can XOR it with the sign bit of x to determine if an overflow will occur
  int hasSameSign = !!((x ^ y) >> 31);
  //int greaterThan = ((~y + 1) + x) >> 31;
  //int greaterThanOrEqualTo = greaterThan | !(x ^ y);

  int performSubtraction = x + (~y) + 1;
  int differenceSign = (performSubtraction >> 31) & 0x01;

  return !hasSameSign | !(differenceSign ^ ((x >> 31) & 0x01));
}
/* howManyBits - return the minimum number of bits required to represent x in
 *             two's complement
 *  Examples: howManyBits(12) = 5
 *            howManyBits(298) = 10
 *            howManyBits(-5) = 4
 *            howManyBits(0)  = 1
 *            howManyBits(-1) = 1
 *            howManyBits(0x80000000) = 32
 *  Legal ops: ! ~ & ^ | + << >>
 *  Max ops: 90
 *  Rating: 4
 */
// Problem 12
int howManyBits(int x) {
  //we should first remember how to convert into 2's complement.
  //twosComplement = ~x + 1
  //now we just have to return the number of bits in the converted number
  //the biggest issue now is that we need to do this without loops or recursion...
  //??? I have no idea how to do this one

  //So to complete this function we do a series of shifts, decreasing by factors of 2
  //and by summing these shifts we will get a partial answer that must sometimes be modified by +1
  //to determine if this modifier is nessessary we also implement a counter which traces our shifts
  //and results in some final modifier.

    int counter = (x & ~(x >> 31)) | (~x & (x >> 31));
    int has16Bits = (!!(counter >> 16)) << 4;
    int counter16 = counter >> has16Bits;
    int has8Bits = (!!(counter16 >> 8)) << 3;
    int counter8 = counter16 >> has8Bits;
    int has4Bits = (!!(counter8 >> 4)) << 2;
    int counter4 = counter8 >> has4Bits;
    int has2Bits = (!!(counter4 >> 2)) << 1;
    int counter2 = counter4 >> has2Bits;
    int has1Bit = (!!(counter2 >> 1));
    int counter1 = counter2 >> has1Bit;

    int modifier = counter1 & 0x01;

    return has16Bits + has8Bits + has4Bits + has2Bits + has1Bit + modifier + 1;
}
/* 
 * float_abs - Return bit-level equivalent of absolute value of f for
 *   floating point argument f.
 *   Both the argument and result are passed as unsigned int's, but
 *   they are to be interpreted as the bit-level representations of
 *   single-precision floating point values.
 *   When argument is NaN, return argument..
 *   Legal ops: Any integer/unsigned operations incl. ||, &&. also if, while
 *   Max ops: 10
 *   Rating: 2
 */
// Problem 13
unsigned float_abs(unsigned uf) {
  //for single precision floating point numbers, the first bit is reserved for the sign
  //the next 8 bits are used for the exponent
  //and the remaining 23 bits are used for the significand
  //NaN is determined if the exponent bits are all 1s

  unsigned int NaN = 0xFF << 23;
  unsigned int exponentMask = NaN & uf;
  //unsigned int significandMask = ((1 << 23) + (~0)) & uf;

  if (((uf << 9) != 0) && (NaN == exponentMask)){
    return uf;
  }else{
    unsigned int mask = ~(1 << 31);
    return mask & uf;
  }
}
/* 
 * float_twice - Return bit-level equivalent of expression 2*f for
 *   floating point argument f.
 *   Both the argument and result are passed as unsigned int's, but
 *   they are to be interpreted as the bit-level representation of
 *   single-precision floating point values.
 *   When argument is NaN, return argument
 *   Legal ops: Any integer/unsigned operations incl. ||, &&. also if, while
 *   Max ops: 30
 *   Rating: 4
 */
// Problem 14
unsigned float_twice(unsigned uf) {
  //normally, to multiply some binary value by 2, you complete a leftshift of 1
  //for this problem however, we must also consider the structure of a single-precision floating point
  //the most significant bit is reserved for the sign
  //the next 8 bits are resered for the exponent
  //the significand is determined by the final 23 bits
  //as a result we can simply add 1 to the 8 bits used for exponent.
  unsigned int NaN = 0xFF << 23;
  unsigned int exponentMask = NaN & uf;
  //unsigned int significandMask = ((0x01 << 23) + (~0)) & uf;

  if (((NaN == exponentMask)) || uf == 0x00){
    return uf;
    //we can utilize XOR and leftshifts to create a mask which looks like: 1 0000 0000 1111 1111 1111 1111 1111 111
    //which is then used to remove the old exponent portion of the float. We have saved the old exponent as shiftedU
    //to which we add 1, creating our new exponent value. We then shift it back into place and combine it to the rest of our
    //number using &.
  }else if (exponentMask == 0){
    unsigned int significandMask = ((0x01 << 23) + (~0)) & uf;
    unsigned int shiftedSignificand = significandMask << 1;
    return (uf & (~significandMask)) + shiftedSignificand;
  }else{
    return uf + (0x01 << 23);
  }
}
/*
 * trueFiveEighths - multiplies by 5/8 rounding toward 0,
 *  avoiding errors due to overflow
 *  Examples: trueFiveEighths(11) = 6
 *            trueFiveEighths(-9) = -5
 *            trueFiveEighths(0x30000000) = 0x1E000000 (no overflow)
 *  Legal ops: ! ~ & ^ | + << >>
 *  Max ops: 25
 *  Rating: 4
 */
// Problem 15
int trueFiveEighths(int x){
  //dividing an int by 8 is simple enough, we must simply rightshift the number 3 times.
  //however this only works for unsigned ints. Therefore if we convert the signed int into an unsigned int
  //by using 2's complement conversion, then complete our rightshift before converting back, we'll account for any
  //signed ints.

  int divBy2 = x >> 1;
  int divBy8 = x >> 3;

  int negativeAdjustment = (x >> 31) & 0x07;
  int divBy2Remainder = (x & 0x01) << 2;
  int divBy8Remainder = x & 0x07;
  int carryCheck = divBy2Remainder + divBy8Remainder;

  return divBy2 + divBy8 + ((negativeAdjustment + carryCheck) >> 3);
}