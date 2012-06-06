guard :shell do
  watch /(rapidmachine|tests)\/.*\.py/ do
    `nosetests --with-yanc --with-xtraceback --with-cov --cov rapidmachine tests`
  end
  watch /docs\/.*\.rst/ do
    `cd docs && make html`
  end
end
