guard :shell do
  watch /(rapidmachine|tests)\/.*\.py/ do
    system 'clear'
    `nosetests --with-yanc --with-xtraceback --with-cov --cov rapidmachine tests`
  end
  watch /docs\/.*\.rst/ do
    system 'clear'
    `cd docs && make html`
  end
end
