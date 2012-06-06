guard :shell do
  watch /(rapidmachine|tests)\/.*\.py/ do |m|
    `nosetests --with-yanc --with-xtraceback --with-cov --cov rapidmachine tests`
  end
end
