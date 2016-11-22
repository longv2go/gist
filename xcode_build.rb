# Build the static lib
#
# @param  [String] project
#         The project path which own the scheme
#
# @param  [String] scheme
#         The scheme name to build
#
# @param [String] config
#         The configuration of the project. 'Release', 'Debug' or others
#
# @param [Array] archs
#
# @return [Pathname] The frameword path
#
ARCHS = [:x86_64, :i386, :armv7s, :armv7, :arm64]
def build_framework(project, scheme, config, defines=nil, output=nil, archs=ARCHS)
    arch2sdk = {i386:'iphonesimulator', x86_64:'iphonesimulator', armv7:'iphoneos', arm64:'iphoneos' , armv7s:'iphoneos'}

    derived_dir = Pathname.new("/tmp/derived_dir")
    derived_dir.exist? && derived_dir.rmtree
    FileUtils.mkdir_p derived_dir.to_s
    FileUtils.mkdir derived_dir + "products" if !(derived_dir + "products").exist?

    #start to build
    archs.each do |arch|
        sdk = arch2sdk[arch]
        command = "xcodebuild #{defines} VALID_ARCHS=#{arch} -sdk #{sdk} PLATFORM_NAME=#{sdk} -project #{project} -arch #{arch} -scheme #{scheme}  -derivedDataPath #{derived_dir.cleanpath} -configuration #{config} build >&2"

        p command
        `#{command}`
        return nil if $?.to_i != 0

        framework_source = derived_dir.to_s  + "/Build/Products/#{config}-#{sdk}/#{scheme}/#{scheme}.framework"
        framework_path = Pathname.new(framework_source)
        if ! framework_path.exist?
          framework_path = Pathname.new(derived_dir.to_s  + "/Build/Products/#{config}-#{sdk}/#{scheme}.framework")
        end

        FileUtils.mv  framework_path.to_s, derived_dir.to_s + "/products/#{scheme}-#{arch}.framework"
    end

    # 合并多个静态库
    output = Pathname.new(output).expand_path if !output.nil?
    if output
      final_out = output.to_s.end_with?('.framework') ? output : output + "#{scheme}.framework"
    else
      final_out =  derived_dir + "products/#{scheme}.framework"
    end

    Dir.chdir((derived_dir + 'products').to_s) do
      libs = Dir.glob("#{scheme}*.framework")
      if libs
        FileUtils.cp_r libs.first, final_out.to_s
        libs = libs.map {|f| "#{f}/#{scheme}"}.join(' ')
        `lipo -create #{libs} -output #{final_out}/#{scheme}`
        final_out = nil if $?.to_i != 0
      end
    end
    return final_out
end
