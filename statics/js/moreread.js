const readMorePrefaceMaxLength = 1000;
const readMoreTexts = document.querySelectorAll(".read-more-text");
readMoreTexts.forEach((readMoreText) => {
  const extra = SliceHTML.sliceHTML(
    readMoreText,
    readMorePrefaceMaxLength
  );
  if (extra.textContent.length === 0) {
    return;
  }
  const preface = SliceHTML.sliceHTML(
    readMoreText,
    0,
    readMorePrefaceMaxLength
  );
  readMoreText.innerHTML = "";
  readMoreText.append(preface);
  const extraSpan = document.createElement("span");
  extraSpan.hidden = true;
  extraSpan.append(extra);
  const p = document.createElement("p");
  p.classList.add("read-more-button");
  p.textContent = "... Read more";
  p.addEventListener("click", () => {
    p.hidden = true;
    extraSpan.hidden = false;
  });
  readMoreText.append(p);
  readMoreText.append(extraSpan);
  
});