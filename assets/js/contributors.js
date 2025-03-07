(async () => {
  function h(tag, props, ...children) {
    const el = document.createElement(tag);
    if (props) {
      for (const key in props) {
        if (props[key]) {
          if (key.startsWith("on")) {
            el[key] = props[key];
          } else {
            el.setAttribute(key, props[key]);
          }
        }
      }
    }
    for (const child of children) {
      if (typeof child === "string") {
        el.appendChild(document.createTextNode(child));
      } else {
        el.appendChild(child);
      }
    }
    return el;
  }

  const response = await fetch(
    "https://api.github.com/repos/WuKongSecurity/WuKongSecurity.github.io/contributors?per_page=100"
  );
  const data = await response.json();

  const contributors = document.querySelector(".contributors");

  data.forEach(result => {
    contributors.appendChild(
      h(
        "a",
        {
          id: result.id,
          class: "contributor",
          href: result.html_url,
          title: `${result.login} GitHub profile`
        },
        h(
          "div",
          { class: "contributor-ratio" },
          h("img", { src: result.avatar_url, alt: `${result.login} avatar` }),
          h(
            "div",
            {
              class: "contributor-hover"
            },
            h("p", {}, result.login),
            h("p", {}, "Contributions: ", String(result.contributions))
          )
        )
      )
    );
  });
  for (let i = 0; i < 10; i += 1) {
    contributors.appendChild(h("div", { class: "contributor-filler" }));
  }
})();
