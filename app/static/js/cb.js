function modexp(base, exponent, modulus)
  {
    var a = base % modulus;
    var b = exponent;
    var result = 1;
    var x = a;

    while(b > 0){
    var lead = b % 2;
    b = Math.floor(b / 2);
    if (lead === 1) {result = result * x; result = result % modulus;}
    x = x * x;
    x = x % modulus;
  }
  return result;
  }

function hash(a)
  {
    var s=a.toUpperCase();
    var n = 1337; var m = 99524506582793;
    for (i = 0; i < s.length; ++ i)
    {
      var k = s.charCodeAt(i);
      if((48 <= k && k <= 57) || (65 <= k && k <= 90)) {n = modexp(n, k, m);}
    }
    return ("xxxxxxxxxxxx" + n.toString(16)).slice(-12);
  }

function verify(answer, h)
  {
    if (hash(answer) == h) 
    {
      alert('Congratulation. You got the right answer.');
      var page = './' + hash('x' + answer);
      location.href = page;
    }
    else
    {
      alert('Invalid.');
    }
  }

