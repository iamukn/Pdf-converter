$(document).ready(() => {
  

// Dynamic quotes function from the type.fit API
const url = 'https://type.fit/api/quotes'

const quote = (x, y) => { 
	$.get(url, (data, status) => {
      const res = data;
      const body = JSON.parse(res);

      //logic to generate the random text
      const len = body.length;
      let rand = Math.floor(Math.random() * 20);
      if (body[rand].text == null || body[rand].author == null) {
      	  $(y).text('Man Know Thyself');
      	  $(x).text('-Socrates-');
      }
      else {
      $(x).text(`-${body[rand].author}-`);
      $(y).text(body[rand].text)
      }
	});
};
quote('#author','#quotes');


// End of dynamic quotes function from the type.fit API
});