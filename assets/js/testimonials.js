(() => {
  function h(tag, props, ...children) {
    const el = document.createElement(tag);
    if (props) {
      for (const key in props) {
        if (props[key]) el.setAttribute(key, props[key]);
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

  function buildTestimonials(testimonialsRoot) {
    function q(selector) {
      return testimonialsRoot.querySelector(selector);
    }

    function matches(el, selector) {
      while (el && el !== testimonialsRoot) {
        if (el.matches(selector)) return el;
        el = el.parentNode;
      }
      return false;
    }

    const testimonials = Array.from(
      testimonialsRoot.querySelectorAll(".testimonials-wrapper .testimonial")
    );

    let focusNextTestimonial = () => {};
    let focusPreviousTestimonial = () => {};

    function focusTestimonial(n) {
      n = (n + testimonials.length) % testimonials.length;
      const hasNext = n !== testimonials.length - 1;
      const hasPrevious = n !== 0;
      const testimonial = testimonials[n];
      const wrapper = q(".testimonials-wrapper");

      // Read
      const containerRect = wrapper.getBoundingClientRect();
      const testimonialRect = testimonial.getBoundingClientRect();

      // Write
      const focused = q(".testimonial.focus");
      if (focused) focused.classList.remove("focus");
      testimonial.classList.add("focus");
      q(".testimonials-wrapper").style.transform =
        "translate(" + (containerRect.left - testimonialRect.left) + "px)";
      q(".next").classList.toggle("disabled", !hasNext);
      q(".previous").classList.toggle("disabled", !hasPrevious);
      const focusedIcon = q(".testimonial-icon.focus");
      if (focusedIcon) focusedIcon.classList.remove("focus");
      q(".testimonial-icon:nth-child(" + (n + 1) + ")").classList.add("focus");

      focusNextTestimonial = () => hasNext && focusTestimonial(n + 1);
      focusPreviousTestimonial = () => hasPrevious && focusTestimonial(n - 1);
    }

    testimonialsRoot.addEventListener("click", event => {
      const testimonial = matches(event.target, ".testimonial");
      if (testimonial) {
        focusTestimonial(testimonials.indexOf(testimonial));
      } else if (matches(event.target, ".previous")) {
        focusPreviousTestimonial();
      } else if (matches(event.target, ".next")) {
        focusNextTestimonial();
      } else {
        const icon = matches(event.target, ".testimonial-icon");
        if (icon) {
          focusTestimonial(Array.from(icon.parentNode.children).indexOf(icon));
        }
      }
    });

    testimonialsRoot.appendChild(
      h(
        "div",
        { class: "testimonials-controls" },
        h(
          "div",
          null,
          h("span", { class: "previous" }),
          h("span", { class: "next" })
        ),
        h(
          "div",
          {
            class: "testimonials-icons"
          },
          ...testimonials.map(() => h("div", { class: "testimonial-icon" }))
        )
      )
    );
    focusTestimonial(0);
  }

  document.querySelectorAll(".testimonials").forEach(buildTestimonials);
})();
