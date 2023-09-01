const readMorePrefaceMaxLength = 150;
const readMoreTexts = document.querySelectorAll(".read-more-text-chat");
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
  p.classList.add("read-more-button-chat");
  p.textContent = "...";
  p.addEventListener("click", () => {
    p.hidden = flase;
    extraSpan.hidden = false;
  });
  readMoreText.append(p);
  readMoreText.append(extraSpan);
  
});